import logging
import argparse
import json
import pandas as pd

from src.data_collection.sarouty_scraper import SaroutyScraper
from src.data_collection.setup_driver import setup_driver


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def parse_parameters():
    """
    Parses parameters from the command line.

    Returns
    -------
    tuple
      (bucket_name, source, selected_params)
    """

    cmd_arg_parser = argparse.ArgumentParser(allow_abbrev=False)

    cmd_arg_parser.add_argument('--source', type=str, required=True,
                                help='Source of the data (Apple or Google)')
    cmd_arg_parser.add_argument('--param', type=str, required=True,
                                help='JSON string containing parameters for both Apple and Google')

    args = cmd_arg_parser.parse_args()
    param_dict = json.loads(args.param)
    args.param_dict = param_dict
    return args


def main_collection(args):
    if args.source == 'Sales':
        url_sales_template = args.param_dict.get("url_sales_template")
        Sales_pages = int(args.param_dict.get("Sales_pages", 1))
        dest_path_sales_path = args.param_dict.get("dest_path_sales_path")
        sales_filename = args.param_dict.get("sales_filename")
        driver = setup_driver()
        sales_data = SaroutyScraper.scrape_all_pages(driver, Sales_pages, url_sales_template, dest_path_sales_path, sales_filename)
        sales_df = pd.DataFrame(sales_data)
        SaroutyScraper.save_data(sales_df, dest_path_sales_path,sales_filename)
        logging.info("Sales Data scrapped and saved successfully.")
    elif args.source == 'Rent':
        url_rent_template = args.param_dict.get("url_rent_template")
        logging.info("url_rent_template: %s", url_rent_template)
        rent_pages = int(args.param_dict.get("rent_pages", 1))
        dest_path_rent_path = args.param_dict.get("dest_path_rent_path")
        rent_filename = args.param_dict.get("rent_filename")
        driver = setup_driver()
        rent_data = SaroutyScraper.scrape_all_pages(driver, rent_pages, url_rent_template, dest_path_rent_path, rent_filename)
        rent_df = pd.DataFrame(rent_data)
        SaroutyScraper.save_data(rent_df, dest_path_rent_path, rent_filename)
        logging.info("rent Data scrapped and saved successfully.")

    else:
        raise ValueError("Source not found in provided parameters.")


main_collection(parse_parameters())
