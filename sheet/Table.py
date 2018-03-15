from gspread import Worksheet

from sheet import AbstractSpreadAccess
from sheet.TableRow import TableRowEntry
import random


class Table(object):
    GSPREAD_READ_RANGE = 10
    GSPREAD_CHANCE_COLUMN = "A{}:A{}"
    GSPREAD_TEXT_COLUMN = "B{}:B{}"

    def __init__(self, table_name: str):
        """ Constructor for a table row entry

        :param table_name the name of the table. The name will be also used as identifier of the table and represents
        an excel sheet
        """
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
        # create the table with all the rows
        table = Table(table_name)
        i = 1
        has_data = True
        while has_data:
            # it is quicker to access the sheet in a range (compared to the cells) -> but it is still slow...
            chances = excel_sheet.range(Table.GSPREAD_CHANCE_COLUMN.format(i, i + Table.GSPREAD_READ_RANGE))
            texts = excel_sheet.range(Table.GSPREAD_TEXT_COLUMN.format(i, i + Table.GSPREAD_READ_RANGE))
            for j, tmp in enumerate(chances):
                text = texts[j].value
                chance = tmp.value
                # found the end in the sheet
                if not text and not chance:
                    has_data = False
                    break
                # illegal configuration (either a chance or the text is missing in the configuration)
                if not chance or not text:
                    raise AttributeError(
                        "Found illegal configuration in the {} in row {}. (Chance = '{}', text = '{}'). ".format(
                            table_name, i, chance, text) + "Chance and Text must be set both!")
                table.add_table_row(TableRowEntry(spread_access, int(chance), text))
            i += Table.GSPREAD_READ_RANGE + 1
        return table
