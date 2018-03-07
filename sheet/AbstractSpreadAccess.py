import abc


class AbstractSpreadAccess(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def crawl_column(self, column_position: int) -> list:
        """This method crawls the column in the main sheet of the crawler. The column defines the context / story
        to be crawled (e.g. a treasure might contain gems, coins, ...).
        Every cell in the column contains a table that is part of the context.

        :param column_position the position of the column in the core excel document
        :return a list with all table names in the column
        """
        pass

    @abc.abstractmethod
    def crawl_table(self, table_name: str) -> None:
        """ This method crawls the table to the given table name, if the table is not known yet.
        The table contains two columns (chance / text) and multiple rows

        :param table_name the name of the table
        """
        pass

    @abc.abstractmethod
    def table_access(self) -> dict():
        """ :return all known table names to their tables"""
        pass

    @abc.abstractmethod
    def story_context(self, column_position: int) -> str:
        """
        :param column_position the position of the column of the current story context
        :return the name of the story """
        pass
