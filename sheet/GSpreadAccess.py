import gspread
import logging
from gspread import Worksheet, WorksheetNotFound, SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
from requests.structures import CaseInsensitiveDict

from core.RpgCrawler import RpgCrawler
from sheet.AbstractSpreadAccess import AbstractSpreadAccess
from sheet.Table import Table


class GSpreadAccess(AbstractSpreadAccess):
    COLUMN_STORY_TABLES = int(1)
    COLUMN_STATIC_PRE_TEXT = int(2)
    COLUMN_STATIC_FOLLOW_UP_TEXT = int(3)
    START_ROW = int(5)
    DEFAULT_SHEET_NAME = "Sheet1"
    CACHE_TABLE_ACCESS_PATTERN = "{}#{}"


    def __init__(self, core_excel_sheet_name: str, permission_file: str,
                 scope: str = 'https://spreadsheets.google.com/feeds') -> None:
        """ Constructor
        Uses the credentials to create access to the given core sheet that contains all contexts / stories

        :param core_excel_sheet_name the name to the core sheet
        :param permission_file the path to the permission file that allows to access the google excel documents#
        :param scope the scope for the service account credentials
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(permission_file, scope)
        self.__table_cache = CaseInsensitiveDict()
        self.__worksheet_cache = CaseInsensitiveDict()
        self.__client = gspread.authorize(credentials)
        self.__core_spread_sheet = self.__client.open(core_excel_sheet_name)
        # the story / context sheet that defines what tables will be used
        self.__context_sheet = self.__core_spread_sheet.sheet1
        self.__core_excel_sheet_name = core_excel_sheet_name
        self.__context_name = ""
        self.__logger = logging.getLogger(RpgCrawler.ID)


    def crawl_main_sheet(self) -> list:
        """This method crawls the main sheet of the generator. The sheet contains static texts and the concatenation of
        the story sheets. Each story sheet is in the same excel sheet (yet). (e.g. a treasure might contain gems,
        coins, ...). Every row in the column contains a table that is part of the context. The format of the main sheet
        is <referenced_table_sheet> <static pre text (optional)> <static followup text (optional)>

        :return a list with all table names in the column
        """
        column_data = self.__context_sheet.col_values(
            GSpreadAccess.COLUMN_STORY_TABLES)  # TODO optimize: only read few cells ...
        crawled_main_sheets = list()
        row = GSpreadAccess.START_ROW
        for table_name in column_data[4:]:
            if not table_name:
                break
            crawled_main_sheets.append(table_name)
            self.__crawl_main_sheet_data(table_name=table_name, row=row)
            row += 1
        return crawled_main_sheets


    def __crawl_main_sheet_data(self, table_name: str = "", row: int = None) -> None:
        """ This method crawls the main tables of the current sheet to the given table name, if the table is not known
        yet. The main tables of the story contain the referenced table name inside the current excel sheet, a pre-text
        and a follow-up text.

        :param table_name the name of the table within the current excel sheet
        :param row the optional row.
        """
        # the table is already known
        if table_name in self.__table_cache:
            return
        # creates a table with rows from the excel sheet
        pre_text = ""
        follow_up_text = ""

        # if a row is specified, we might have pre and follow up texts to the current story context
        if row is not None:
            pre_text = self.__context_sheet.cell(row, GSpreadAccess.COLUMN_STATIC_PRE_TEXT).value
            follow_up_text = self.__context_sheet.cell(row, GSpreadAccess.COLUMN_STATIC_FOLLOW_UP_TEXT).value

        table = Table.from_sheet(self, table_name, GSpreadAccess.DEFAULT_SHEET_NAME, pre_text, follow_up_text)
        # in case of an empty sheet
        if len(table.table_rows) is 0:
            raise ValueError(
                "In der referenzierten Storytabelle '{}' konnten keine Zeilen identifiziert werden.".format(table_name))
        self.__table_cache[table_name] = table


    def __crawl_table_data(self, table_name: str, sheet_name: str = DEFAULT_SHEET_NAME) -> None:
        """ This method crawls the table to the given table name, if the table is not known yet.
        The table contains two columns (chance / text) and multiple rows.

        :param table_name the name of the table. In some contexts the name of the table can be the excel file name
        :param sheet_name optional possibility to access the sheet by name in a different excel file
        """
        if table_name in self.__table_cache:
            return

        table = Table.from_sheet(self, table_name, sheet_name)
        # in case of an empty sheet
        if len(table.table_rows) is 0:
            raise ValueError(
                "In der Tabelle '{}' zu dem Sheet '{}'".format(table_name, sheet_name) +
                " konnten keine Zeilen identifiziert werden.")

        self.__logger.debug("Cache die Tabelle mit dem Namen {}".format(table_name))
        self.__table_cache[table_name] = table


    def crawl_sheet_column_in_range(self, table_name: str, sheet_name: str, column_pattern: str, row_pos: int) -> list:
        """ This method crawls in a specified read range from the given row position and returns the values. Empty lines
        will be read too.

        :param table_name the name of the table to crawl
        :param sheet_name optional possibility to access the sheet by name in a different excel file
        :param column_pattern the range pattern that is used to access multiple cells in a columns. (e.g. A{}:A{})
        :param row_pos the position of the row where we start to crawl
        :return a list with values.
        """
        # the current sheet contains a table with chances and texts
        excel_sheet = self.__determine_table_sheet(table_name, sheet_name)
        column_data = list()
        # it is quicker to access the sheet in a range (compared to the cells) -> but it is still slow...
        all_column_data = excel_sheet.range(column_pattern.format(row_pos, row_pos + self.read_range))
        for idx, tmp in enumerate(all_column_data):
            column_data.append(tmp.value)
        return column_data


    def __determine_table_sheet(self, table_name: str, sheet_name: str = DEFAULT_SHEET_NAME) -> Worksheet:
        """ This method determines the the sheet by the given table name.
        In the first try, the method will try to open a spread sheet within the core excel sheet as a tab.
        If the the excel sheet tab doesn't exist within the core excel sheet the method will try to open a
        excel file and return the sheet1. In case, the sheet_name is defined, the method will try to find the sheet
        by name

        :param table_name the name of the table to open
        :param sheet_name optional possibility to access the sheet by name in a different excel file
        :return the work sheet / spread sheet
        """
        # is it cached?
        direct_cache_name = GSpreadAccess.CACHE_TABLE_ACCESS_PATTERN.format(self.__core_excel_sheet_name, table_name)
        if direct_cache_name in self.__worksheet_cache:
            return self.__worksheet_cache[direct_cache_name]
        excel_cache_name = GSpreadAccess.CACHE_TABLE_ACCESS_PATTERN.format(table_name, sheet_name)
        if excel_cache_name in self.__worksheet_cache:
            return self.__worksheet_cache[excel_cache_name]

        # not cached yet. Load it
        try:
            # first try - verify if the table name is inside of the core sheet
            sheet = self.__core_spread_sheet.worksheet(table_name)
            # cache
            self.__worksheet_cache[direct_cache_name] = sheet
        except WorksheetNotFound:
            # second try - try to open a a different excel file to the sheet name
            try:
                sheet = self.__client.open(table_name).worksheet(sheet_name)
                # cache
                self.__worksheet_cache[excel_cache_name] = sheet
            except SpreadsheetNotFound:
                raise ValueError(
                    "Zu dem Tabellenname '{}' bzw. dem Sheet '{}' konnte weder ein Excel-Sheet noch eine Excel-Datei "
                    .format(table_name, sheet_name) +
                    "gefunden werden. Der Tabellenname muss identisch sein!")
        return sheet


    def story_context(self) -> str:
        """ Determines the story context of the sheet in the first column / first row

        :return the context / name of the story """
        if not self.__context_name:
            self.__context_name = self.__context_sheet.col_values(1)[0]
        return self.__context_name


    def get_table(self, table_name: str, sheet_name: str = DEFAULT_SHEET_NAME):
        """ This method verifies if a table exists. If yes, the table will be returned. If not, the table will be
        crawled, cached and returned afterwards

        :param table_name the name of the table
        :param sheet_name optional possibility to access the sheet by name in a different excel file
        :return the table
        """
        if table_name not in self.table_access:
            self.__crawl_table_data(table_name, sheet_name)
        return self.table_access[table_name]


    @property
    def table_access(self) -> CaseInsensitiveDict():
        """:return all known table names to their tables"""
        return self.__table_cache


    @property
    def read_range(self) -> int:
        """
        Determines the range of rows to be read. This is required since the access on the spread sheet might
        be very slow. Due to this, rows will be read in chunks

        :return the range of rows to be read"""
        return 10


    @property
    def chance_range_column_pattern(self) -> str:
        """:return the range pattern for the chance column in data tables """
        return "A{}:A{}"


    @property
    def text_range_column_pattern(self) -> str:
        """:return the range pattern for the text column in data tables """
        return "B{}:B{}"
