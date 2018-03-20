import abc


class AbstractGenerator(metaclass=abc.ABCMeta):
    def __init__(self, start_index: int, end_index: int, text: str) -> None:
        """
        Constructor

        :param start_index the start position in the original text string
        :param end_index the end position in the original text string
        :param text the text for the generator
        """
        self.__start_index = start_index
        self.__end_index = end_index
        self.__text = text


    @abc.abstractmethod
    def process(self) -> str:
        """ Generates the value

        :return the generated result"""
        pass


    def replace_offset_of(self, generated_text: str) -> int:
        """ determines the offset between the generated value and the text to replace.

        :param generated_text the generated text
        :return the offset
        """
        # 2 because next to the text we have the braces that must be replaced
        return len(generated_text) - (len(self.__text) + 2)


    @property
    def get_start_index(self):
        """ :return: start the start position in the original text string """
        return self.__start_index


    @property
    def get_end_index(self):
        """ :return: end the end position in the original text string """
        return self.__end_index


    @property
    def get_text(self):
        """ :return: text the text for the generator """
        return self.__text
