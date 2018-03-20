import random
import re

from generator.AbstractGenerator import AbstractGenerator


class DiceThrow(AbstractGenerator):
    PATTERN = "^\d{1,3}\s*[w]\s*\d{1,3}$"


    def __init__(self, start_index: int, end_index: int, text: str) -> None:
        AbstractGenerator.__init__(self, start_index, end_index, text)
        """ Constructor:
        Defines the parameters for a dice throw

        :param start_index the start position in the original text string
        :param end_index the end position in the original text string
        :param text if quantity and dice are not specified, the information will be extracted from the text. 
        The text has the format of quantity w dice. The quantity defines, how often a dice will be thrown,
        e.g. [3W6] -> throws a d6 3 times. The dice define the dice to be thrown
        """
        details = re.split("W", text, flags=re.IGNORECASE)
        self.__quantity = int(details[0])
        self.__dice = int(details[1])


    def process(self) -> str:
        """ Throws a specified dice x times

        :return the dice result"""
        value = 0
        # calculates the dice value
        for _i in range(self.__quantity):
            # +1 because random expects a value that is higher
            value += random.randint(1, self.__dice + 1)
        return str(value)
