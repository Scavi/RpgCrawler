import re

from generator.DiceThrow import DiceThrow
from generator.TableReference import TableReference
from sheet import AbstractSpreadAccess


class TableRowEntry(object):
    def __init__(self, spread_access: AbstractSpreadAccess, chance: int, text: str):
        """ Constructor for a table row entry

        :param spread_access the access to the spreads
        :param chance -- a number that represents the probability of all entries within this table to get picked
        :param text -- the text of this row
        """
        self.__chance = chance
        self.__text = text
        self.__generators = TableRowEntry.analyze_generators(spread_access, text)

    @staticmethod
    def analyze_generators(spread_access: AbstractSpreadAccess, text: str) -> list:
        """
        Parses the string and determines all generators (in the format of [...]). Returns all the generator in the order
        they occur in the given string.
        Supported generator pattern are:
        DiceThrow, e.g. [4W12]

        :param spread_access the access to the spreads
        :param text the text to analyze
        :return a list of all pattern.
        """
        if not text:
            return list()
        generator_pattern = re.compile("(?<=\[)[^\]]*")

        result = list()
        for matcher in generator_pattern.finditer(text):
            generator_match = matcher.group()

            start_index = matcher.start() - 1
            end_index = matcher.end()

            # matches the dice throw pattern
            if re.match(DiceThrow.PATTERN, generator_match, re.IGNORECASE):
                # -1 to include the [ of the string
                result.append(DiceThrow(start_index, end_index, generator_match))
            elif re.match(TableReference.PATTERN, generator_match, re.IGNORECASE):
                result.append(TableReference(spread_access, start_index, end_index, generator_match))
        return result

    def __str__(self) -> str:
        """ :return representation for the class """
        return "{} -> {}".format(self.__chance, self.__text)

    def __repr__(self) -> str:
        """ :return representation for debugging """
        return self.__str__()

    def generate(self):
        offset = 0
        result = self.__text
        for generator in self.__generators:
            tmp = generator.process()
            result = result[0:generator.get_start_index + offset] + tmp + result[generator.get_end_index + offset + 1:]
            offset += generator.replace_offset_of(tmp)
        return result

    @property
    def get_chance(self) -> int:
        """ :return a number that represents the chance / probability of all entries within this table to get picked """
        return self.__chance

    @property
    def get_text(self) -> str:
        """ :return the text of this row """
        return self.__text
