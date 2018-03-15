from interaction.AbstractIO import AbstractIO


class ConsoleIO(AbstractIO):

    def print_story_context(self, context: str) -> None:
        """ This method prints the story context

        :param context the context to be printed (e.g. the small treasure in the dragons lair)
        """
        print(context)

    def print_story_line(self, story_line: str) -> None:
        """ This method prints the story line with a small indent

        :param story_line the story line to be printed (e.g. you found 2 gold and 20 silver in the chest)
        """
        print("\t" + story_line)

    def determine_column(self) -> int:
        """ This method determines the column in the sheet to process (starting with 1)

        :return the column to process
        """
        column = input("\nWelche Spaltennummer soll verarbeitet werden? (1 (für Spalte A), 2 (für Spalte B) usw.): ")
        # TODO: currently it is only simple console application. In case UI will be added, MVP / MVP should be used
        if not column.isdigit() or int(column) < 1:
            print("Die Spalteneingabe war fehlerhaft. Bitte die Spaltennummer angeben!")
            return self.determine_column()
        else:
            return int(column)
