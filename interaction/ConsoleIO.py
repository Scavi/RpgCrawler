from interaction.AbstractIO import AbstractIO
from sheet.Table import Table


class ConsoleIO(AbstractIO):

    def print_story_context(self, context: str) -> None:
        """ This method prints the story context

        :param context the context to be printed (e.g. the small treasure in the dragons lair)
        """
        print(context)


    def print_story_line(self, table: Table) -> None:
        """ This method prints the story line with a small indent

        :param table the table to process
        """
        text = self.create_table_text(table)
        print(text)


    def create_table_text(self, table: Table) -> str:
        """ Creates the current text line. Depending on the configuration, the text line contains the table name,
        an optional static pre text, the generated row and an optional static follow up text.
        -> e.g. "Freitext vor Tabelle Aktion Freitext nach Tabelle Aktion"

        :param table the table data
        :return the text to write
        """
        # determines the current row by chance
        table_row = table.get_row_by_chance()
        row_text = "\t{}:\n".format(table.table_name)
        if table.pre_text:
            row_text += "\t{}\n".format(table.pre_text)
        row_text += "\t{}\n".format(table_row.generate())
        if table.follow_up_text:
            row_text += "\t{}\n".format(table.follow_up_text)
        return row_text

    # def create_table_text(self, table: Table) -> str:
    #     """ Creates the current text line. Depending on the configuration, the text line contains the table name,
    #     an optional static pre text, the generated row and an optional static follow up text.
    #     -> e.g. "Freitext vor Tabelle Aktion Freitext nach Tabelle Aktion"
    #
    #     :param table the table data
    #     :return the text to write
    #     """
    #     # determines the current row by chance
    #     table_row = table.get_row_by_chance()
    #     row_text = table.table_name + ": "
    #     if table.pre_text:
    #         row_text += "{} ".format(table.pre_text)
    #     row_text += table_row.generate()
    #     if table.follow_up_text:
    #         row_text += " {}".format(table.follow_up_text)

    def iterations(self) -> int:
        """ This method determines the iterations of the application (e.g. execute 5 times)

        :return the iterations
        """
        iteration = input("\nWieviele Iterationen sollen durchgeführt werden (0 = Programmende): ")
        # TODO: currently it is only simple console application. In case UI will be added, MVP / MVP should be used
        if not iteration.isdigit():
            print("Die Eingabe war fehlerhaft! Bitte einen numerischen Wert eingeben!")
            return self.iterations()
        else:
            return int(iteration)
