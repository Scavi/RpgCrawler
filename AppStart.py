import os

from core.RpgCrawler import RpgCrawler
from interaction.AbstractIO import AbstractIO
from interaction.ConsoleIO import ConsoleIO
from sheet.AbstractSpreadAccess import AbstractSpreadAccess
from sheet.GSpreadAccess import GSpreadAccess


def create_spread_access() -> AbstractSpreadAccess:
    """Creates the access to the spread sheet. Uses the permission file for the spread sheet acces

    :return the spread sheet access
    """
    root_path = os.path.dirname(os.path.realpath(__file__))
    permission_path = os.path.join(root_path, 'permissions/RpgCrawler-b8b181033387.json')
    return GSpreadAccess('RpgCrawler', permission_path)


def create_crawler(spread_access: GSpreadAccess, io: AbstractIO) -> RpgCrawler:
    """Creates the crawler that iterates the excel sheets

    :param spread_access the spread sheet access
    :param io the io interaction interface for the user
    :return the excel sheet crawler
    """
    return RpgCrawler(spread_access, io)


def create_io():
    """ the interface to the user (input / output)
    :return the io interface of the user
    """
    return ConsoleIO()


def main():
    """ The main method of the application. Creates the required objects and initiates the program execution """
    io = create_io()
    spread = create_spread_access()
    crawler = create_crawler(spread, io)

    print("=> Zum Beenden der Anwendung Strg+C betätigen!\n")
    while True:
        column = io.determine_column()
        for i in range(1, 6):
            crawler.crawl(column)


if __name__ == '__main__':
    main()
