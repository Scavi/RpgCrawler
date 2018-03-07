import abc


class AbstractIO(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def print_story_context(self, context: str) -> None:
        """ This method prints the story context

        :param context the context to be printed (e.g. the small treasure in the dragons lair)
        """
        pass

    @abc.abstractmethod
    def print_story_line(self, story_line: str) -> None:
        """ This method prints the story line

        :param story_line the story line to be printed (e.g. you found 2 gold and 20 silver in the chest)
        """
        pass

    def print_info(self, text: str) -> None:
        """ This method prints a general information for the user

        :param text the text to print
        """
        pass

    @abc.abstractmethod
    def determine_column(self) -> int:
        """ This method determines the column in the sheet to process (starting with 1)

        :return the column to process
        """
        pass
