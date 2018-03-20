import random

from sheet import AbstractSpreadAccess
from sheet.TableRow import TableRowEntry


class Table(object):
    def __init__(self, table_name: str, pre_text: str = "", follow_up_text: str = ""):
        """ Constructor for a table row entry

        :param table_name the name of the table. The name will be also used as identifier of the table and represents
            an excel sheet
        :param pre_text an optional and static text that will be printed before randomly selected and generated
            table row text
        :param follow_up_text an optional and static text that will be printed after randomly selected and generated
            table row text
        """
        self.__table_name = table_name
        self.__rows = list()
        self.__max_chance = 0
        self.__pre_text = pre_text
        self.__follow_up_text = follow_up_text


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


    def get_row_by_chance(self) -> TableRowEntry:
        """ Calculates the chance and iterates through the list of all rows and determines the row by chance

        :return the row to process """

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
    def table_name(self) -> str:
        """ :return the name of the table. The name will be also used as identifier """
        return self.__table_name


    @property
    def pre_text(self) -> str:
        """ :return an optional and static text that will be printed before randomly selected and generated
            table row text """
        return self.__pre_text


    @property
    def follow_up_text(self) -> str:
        """ :return an optional and static text that will be printed after randomly selected and generated
            table row text """
        return self.__follow_up_text


    @property
    def table_rows(self) -> list:
        """ :return access to the rows of the table """
        return self.__rows


    @staticmethod
    def from_sheet(sheet_access: AbstractSpreadAccess, table_name: str, pre_text: str = "", follow_up_text: str = ""):
        """ This method creates a table object from the given parameters. The excel_sheet has two columns, a chance
        that represents how likely the row will be picked from the table and a text row text that has the information

        :param sheet_access the access to the spreads
        :param table_name the name of the table
        :param pre_text an optional and static text that will be printed before randomly selected and generated
            table row text
        :param follow_up_text an optional and static text that will be printed after randomly selected and generated
            table row text
        :return the created table with all the rows
        """
        # create the table with all the rows
        table = Table(table_name, pre_text, follow_up_text)
        i = 1
        is_reading = True
        while is_reading:
            # it is quicker to access the sheet in a range (compared to the cells) -> but it is still slow...
            chances = sheet_access.crawl_sheet_column_in_range(table_name, sheet_access.chance_range_column_pattern, i)
            texts = sheet_access.crawl_sheet_column_in_range(table_name, sheet_access.text_range_column_pattern, i)
            for j, chance in enumerate(chances):
                text = texts[j]
                # found the end in the sheet
                if not text and not chance:
                    is_reading = False
                    break
                # illegal configuration (either a chance or the text is missing in the configuration)
                if not chance or not text:
                    raise AttributeError(
                        "Die Tabelle '{}' enthält in der Zeile '{}' eine fehlerhafte ".format(table_name, i) +
                        "Konfiguration (Chance = '{}', Text = '{}'). ".format(table_name, i, chance, text) +
                        "Beide Spalten (Chance und Text) müssen gefüllt sein!")
                table.add_table_row(TableRowEntry(sheet_access, int(chance), text))
            i += sheet_access.read_range + 1
        return table
