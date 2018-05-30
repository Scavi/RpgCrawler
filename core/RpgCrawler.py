from interaction.AbstractIO import AbstractIO
from sheet.AbstractSpreadAccess import AbstractSpreadAccess


class RpgCrawler:
    ID = "rpgcrawler.logic"


    def __init__(self, spread_access: AbstractSpreadAccess, formatter: AbstractIO) -> None:
        """ Constructor
        :param spread_access the access to the spread sheet that contains all table to crawl
        :param formatter the formatter for the output
        """
        self.__spread_access = spread_access
        self.__formatter = formatter


    def crawl(self):
        # all the tables of the story that needs to be iterated (e.g. gems, coins, armor of a treasure)
        story_tables = self.__spread_access.crawl_main_sheet()
        self.__formatter.print_story_context(self.__spread_access.story_context())
        for table_name in story_tables:
            # determines the current table (e.g. gems)
            table = self.__spread_access.get_table(table_name)
            self.__formatter.print_story_line(table)
