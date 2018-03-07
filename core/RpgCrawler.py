from interaction.AbstractIO import AbstractIO
from sheet.AbstractSpreadAccess import AbstractSpreadAccess


class RpgCrawler:

    def __init__(self, spread_access: AbstractSpreadAccess, formatter: AbstractIO) -> None:
        self.__spread_access = spread_access
        self.__formatter = formatter

    def crawl(self, column_position: int):
        # all the tables of the story that needs to be iterated (e.g. gems, coins, armor of a treasure)
        story_tables = self.__spread_access.crawl_column(column_position)

        self.__formatter.print_story_context(self.__spread_access.story_context(column_position))

        for table_name in story_tables:
            # determines the current table (e.g. gems)
            table = self.__spread_access.table_access[table_name]
            # determines the current row by chance
            row = table.get_row_by_chance()
            self.__formatter.print_story_line(row.generate())
