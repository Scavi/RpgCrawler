from gspread import Worksheet

from sheet import AbstractSpreadAccess
from sheet.TableRow import TableRowEntry
import random


class Table(object):
    def __init__(self, spread_access: AbstractSpreadAccess, table_name: str):
        """ Constructor for a table row entry

        :param spread_access the access to the spreads
        :param table_name the name of the table. The name will be also used as identifier of the table and represents
        an excel sheet
        """
        self.__spread_access = spread_access
        self.__table_name = table_name
        self.__rows = list()
        self.__max_chance = 0

    def __str__(self) -> str:
        """ :return representation for the class """
        return self.__table_name

    def __repr__(self) -> str:
        """ :return representation for debugging """
        return str(self.__str__())

    def add_table_row(self, row: TableRowEntry) -> None:
        """ Adds a new row to the given table. Increases the overall chanced
         :param row the row to add
         """
        if not row:
            return
        self.__max_chance += row.get_chance
        self.__rows.append(row)

    def get_row_by_chance(self):
        """ Calculates the chance and iterates through the list of all rows and determines the row by chance"""

        #  a value between 1 and __max_chance
        chance = random.randint(1, self.__max_chance + 1)
        row = None
        pos = 0
        while chance > 0 and pos < len(self.__rows):
            row = self.__rows[pos]
            chance -= row.get_chance
            pos += 1
        return row

    @property
    def get_name(self) -> str:
        """ :return the name of the table. The name will be also used as identifier """
        return self.__table_name

    @property
    def table_rows(self) -> list:
        """ :return access to the rows of the table """
        return self.__rows

    @staticmethod
    def from_sheet(spread_access: AbstractSpreadAccess, table_name: str, excel_sheet: Worksheet):
        """ This method creates a table object from the given parameters. The excel_sheet has two columns, a chance
        that represents how likely the row will be picked from the table and a text row text that has the information

        :param spread_access the access to the spreads
        :param table_name the name of the table
        :param excel_sheet the excel sheet that represents the table.
        :return the created table with all the rows
        """
        chances = excel_sheet.col_values(1)
        texts = excel_sheet.col_values(2)

        # the number of chances and texts must be identical
        if len(chances) != len(texts):
            raise AttributeError(
                "Illegal configuration! The count of chances {} and texts {} don't match".format(len(chances),
                                                                                                 len(texts)))

        # create the table with all the rows
        table = Table(spread_access, table_name)
        i = 0
        while True:
            if not texts[i]:
                break
            table.add_table_row(TableRowEntry(spread_access, int(chances[i]), texts[i]))
            i += 1
        return table
