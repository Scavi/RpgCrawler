import os
import sys

from core.RpgCrawler import RpgCrawler
from interaction.AbstractIO import AbstractIO
from interaction.ConsoleIO import ConsoleIO
from sheet.AbstractSpreadAccess import AbstractSpreadAccess
from sheet.GSpreadAccess import GSpreadAccess


def determine_excel_sheet_name() -> str:
    """ Determines the name of the excel sheet to be crawled from the start parameter of the application
    :return the name of the target excel sheet"""
    if len(sys.argv) < 2:
        raise ValueError("Der RpgCrawler erwartet den Namen der Excel-Datei als Aufrufparameter!\n" +
                         "Beispiel: AppStart.exe RpgCrawler")
    return str(sys.argv[1]).strip()


def create_spread_access(spread_sheet_name: str) -> AbstractSpreadAccess:
    """Creates the access to the spread sheet. Uses the permission file for the spread sheet acces
    :return the spread sheet access
    """
    root_path = os.path.dirname(os.path.realpath(__file__))
    permission_path = os.path.join(root_path, 'permissions/RpgCrawler-b8b181033387.json')
    return GSpreadAccess(spread_sheet_name, permission_path)


def create_crawler(spread_access: AbstractSpreadAccess, io: AbstractIO) -> RpgCrawler:
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
    print("#################################################")
    print("######### RPG Crawler v0.40 (06.05.2018) ########")
    print("#################################################")
    excel_sheet_name = determine_excel_sheet_name()
    spread = create_spread_access(excel_sheet_name)
    io = create_io()
    crawler = create_crawler(spread, io)
    while True:
        iteration = io.iterations()
        if iteration == 0:
            break
        for i in range(1, iteration + 1):
            crawler.crawl()


if __name__ == '__main__':
    main()
