import re

from generator.AbstractGenerator import AbstractGenerator
from sheet.AbstractSpreadAccess import AbstractSpreadAccess


class TableReference(AbstractGenerator):
    PATTERN = "\s*Tabelle:.+"

    def __init__(self, spread_access: AbstractSpreadAccess, start_index: int, end_index: int, text: str) -> None:
        AbstractGenerator.__init__(self, start_index, end_index, text)
        """ Constructor:
        Defines the parameters for a dice throw

        :param spread_access the access to the spreads
        :param start_index the start position in the original text string
        :param end_index the end position in the original text string
        :param text if quantity and dice are not specified, the information will be extracted from the text. The text
            has the format of quantity w dice. The quantity defines, how often a dice will be thrown,
            e.g. [3d6] -> throws a d6 3 times. The dice defines the dice to be thrown
        """
        details = re.split("Tabelle:", text.strip(), flags=re.IGNORECASE)
        self.__table_name = details[1].strip()
        self.__spread_access = spread_access

    def process(self) -> str:
        """ Determines a table row by chance from the referenced table and generates the table result
        :return the generated table result"""
        referenced_table = self.__spread_access.table_access[self.__table_name]
        row = referenced_table.get_row_by_chance()
        return row.generate()
