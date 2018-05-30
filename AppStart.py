import os
import logging
import argparse
from core.RpgCrawler import RpgCrawler
from interaction.AbstractIO import AbstractIO
from interaction.ConsoleIO import ConsoleIO
from sheet.AbstractSpreadAccess import AbstractSpreadAccess
from sheet.GSpreadAccess import GSpreadAccess


def create_argument_parser() -> argparse.ArgumentParser:
    """ Creates the argument parser with the mandatory and optional parameters of this application
    :return the argument parser of the application
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", required=False, choices=[True, False], type=bool,
                        help="Ein optionaler Parameter um Debug-Informationen der Anwendung herauszuschreiben.")
    parser.add_argument("--f", required=True,
                        help="Ein erforderlicher Parameter der den Namen des Start Google Sheets angibt.")
    return parser


def determine_excel_sheet_name(arguments: argparse.Namespace) -> str:
    """ Determines the name of the excel sheet to be crawled from the start parameter of the application
    :param arguments the program arguments accessible by argparse
    :return the name of the target excel sheet"""
    return str(arguments.f).strip()


def create_spread_access(spread_sheet_name: str) -> AbstractSpreadAccess:
    """Creates the access to the spread sheet. Uses the permission file for the spread sheet access
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


def init_log(arguments: argparse.Namespace) -> None:
    """ Sets the root logger and the application logger to debug
    :param arguments the program arguments accessible by argparse
    :return:
    """
    if arguments.d:
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        crawl_logic_stream = logging.StreamHandler()
        crawl_logic_stream.setLevel(logging.DEBUG)
        crawl_logic_stream.setFormatter(formatter)
        logging.getLogger(RpgCrawler.ID).setLevel(logging.DEBUG)
        logging.getLogger('').setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(crawl_logic_stream)


def main():
    """ The main method of the application. Creates the required objects and initiates the program execution """
    print("#################################################")
    print("######### RPG Crawler v0.50 (30.05.2018) ########")
    print("#################################################")
    argument_parser = create_argument_parser()
    arguments = argument_parser.parse_args()
    init_log(arguments)
    excel_sheet_name = determine_excel_sheet_name(arguments)
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
