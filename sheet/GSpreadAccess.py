import gspread
from oauth2client.service_account import ServiceAccountCredentials

from sheet.AbstractSpreadAccess import AbstractSpreadAccess
from sheet.Table import Table


class GSpreadAccess(AbstractSpreadAccess):

    def __init__(self, excel_sheet_name: str, permission_file: str,
                 scope: str = 'https://spreadsheets.google.com/feeds') -> None:
        """ Constructor
        Uses the credentials to create access to the given core sheet that contains all contexts / stories

        :param excel_sheet_name the name to the core sheet
        :param permission_file the path to the permission file that allows to access the google excel documents#
        :param scope the scope for the service account credentials
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(permission_file, scope)
        self.__tables = {}
        self.__client = gspread.authorize(credentials)
        self.__sheet = self.__client.open(excel_sheet_name).sheet1

    def crawl_column(self, column_position: int) -> list:
        """This method crawls the column in the main sheet of the crawler. The column defines the context / story
        to be crawled (e.g. a treasure might contain gems, coins, ...).
        Every cell in the column contains a table that is part of the context.

        :param column_position the position of the column in the core excel document
        :return a list with all table names in the column
        """
        column_data = self.__sheet.col_values(column_position)

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
        current_sheet = self.__client.open(table_name).sheet1
        # creates a table with rows from the excel sheet
        table = Table.from_sheet(self, table_name, current_sheet)
        self.__tables[table_name] = table

    def story_context(self, column_position: int) -> str:
        """
        :param column_position the position of the column of the current story context
        :return the name of the story """
        return self.__sheet.col_values(column_position)[0]

    @property
    def table_access(self) -> dict():
        """:return all known table names to their tables"""
        return self.__tables
