import gspread
from gspread import WorksheetNotFound, SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

from sheet.AbstractSpreadAccess import AbstractSpreadAccess
from sheet.Table import Table
from requests.structures import CaseInsensitiveDict


class GSpreadAccess(AbstractSpreadAccess):
    def __init__(self, core_excel_sheet_name: str, permission_file: str,
                 scope: str = 'https://spreadsheets.google.com/feeds') -> None:
        """ Constructor
        Uses the credentials to create access to the given core sheet that contains all contexts / stories

        :param core_excel_sheet_name the name to the core sheet
        :param permission_file the path to the permission file that allows to access the google excel documents#
        :param scope the scope for the service account credentials
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(permission_file, scope)
        self.__tables = CaseInsensitiveDict()
        self.__client = gspread.authorize(credentials)
        self.__core_spread_sheet = self.__client.open(core_excel_sheet_name)
        # the story / context sheet that defines what tables will be used
        self.__context_sheet = self.__core_spread_sheet.sheet1
        self.__core_excel_sheet_name = core_excel_sheet_name

    def crawl_column(self, column_position: int) -> list:
        """This method crawls the column in the main sheet of the crawler. The column defines the context / story
        to be crawled (e.g. a treasure might contain gems, coins, ...).
        Every cell in the column contains a table that is part of the context.

        :param column_position the position of the column in the core excel document
        :return a list with all table names in the column
        """
        column_data = self.__context_sheet.col_values(column_position)

        crawled_tables = list()
        # the first row contains a title / description, not a table name that needs to be crawled
        for table_name in column_data[1:]:
            if not table_name:
                break
            crawled_tables.append(table_name)
            self.crawl_table(table_name)
        return crawled_tables

    def crawl_table(self, table_name: str) -> None:
        """ This method crawls the table to the given table name, if the table is not known yet.
        The table contains two columns (chance / text) and multiple rows

        :param table_name the name of the table
        """
        # the table is already known
        if table_name in self.__tables:
            return
        # the current sheet contains a table with chances and texts
        current_sheet = self.determine_table_sheet(table_name)
        # creates a table with rows from the excel sheet
        table = Table.from_sheet(self, table_name, current_sheet)
        self.__tables[table_name] = table

    def determine_table_sheet(self, table_name: str):
        """ This method determines the the sheet by the given table name.
        In the first try, the method will try to open a spread sheet within the core excel sheet as a tab.
        If the the excel sheet tab doesn't exist within the core excel sheet the method will try to open a
        excel file and return the sheet1.

        :param table_name the name of the table to open
        :return the work sheet / spread sheet
        """
        try:
            return self.__core_spread_sheet.worksheet(table_name)
        except WorksheetNotFound:
            try:
                return self.__client.open(table_name).sheet1
            except SpreadsheetNotFound:
                raise ValueError(
                    "Zu der Tabelle '{}' konnte weder ein Excel-Sheet noch eine Excel-Datei ".format(table_name) +
                    "gefunden werden. Der Tabellenname muss identisch sein!")

    def story_context(self, column_position: int) -> str:
        """
        :param column_position the position of the column of the current story context
        :return the name of the story """
        return self.__context_sheet.col_values(column_position)[0]

    def get_table(self, table_name: str):
        """ this method verifies if a table exists. If yes, the table will be returned. If not, the table will be
        crawled, cached and returned afterwards

        :param table_name the name of the table
        :return the table
        """
        if table_name not in self.table_access:
            self.crawl_table(table_name)
        return self.table_access[table_name]

    @property
    def table_access(self) -> CaseInsensitiveDict():
        """:return all known table names to their tables"""
        return self.__tables
