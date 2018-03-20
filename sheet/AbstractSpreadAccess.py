import abc

from requests.structures import CaseInsensitiveDict


class AbstractSpreadAccess(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def crawl_main_sheet(self) -> list:
        """ This method crawls the column for tables in the main sheet of the crawler.
        The column defines the context / story to be crawled (e.g. a treasure might contain gems, coins, ...).
        Every cell in the column contains a table that is part of the context.

        :return a list with all table names in the column
        """
        pass


    @abc.abstractmethod
    def get_table(self, table_name: str):
        """ this method verifies if a table exists. If yes, the table will be returned. If not, the table will be
        crawled, cached and returned afterwards

        :param table_name the name of the table
        :return the table
        """
        pass


    @abc.abstractmethod
    def table_access(self) -> CaseInsensitiveDict():
        """ :return all known table names to their tables"""
        pass


    @abc.abstractmethod
    def story_context(self) -> str:
        """ :return the context / name of the story """
        pass


    @abc.abstractmethod
    def read_range(self) -> int:
        """
        Determines the range of rows to be read. This is required since the access on the spread sheet might
        be very slow. Due to this, rows will be read in chunks

        :return the range of rows to be read"""
        pass


    @abc.abstractmethod
    def chance_range_column_pattern(self) -> str:
        """:return the range pattern for the chance column in data tables """
        pass


    @abc.abstractmethod
    def text_range_column_pattern(self) -> str:
        """:return the range pattern for the text column in data tables """
        pass
