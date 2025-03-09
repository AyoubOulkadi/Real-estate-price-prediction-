import time
import logging
import pandas as pd
from src.data_collection.setup_driver import setup_driver
from src.data_collection.extract_property_data import extract_property_data
from src.data_collection.save_data import save_to_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class SaroutyScraper:
    def __init__(self, max_pages=158, base_url="https://www.sarouty.ma/acheter/proprietes-a-vendre.html?page="):
        """Initialize the scraper."""
        self.max_pages = max_pages
        self.driver = setup_driver()
        self.base_url = base_url
        self.data = []

    def scrape_all_pages(self):
        """Loop through multiple pages and collect data."""
        logging.info("Starting scraper...")

        for page_number in range(1, self.max_pages + 1):
            try:
                logging.info(f"Scraping page {page_number}...")
                page_data = extract_property_data(self.driver, self.base_url, page_number)
                self.data.extend(page_data)
                time.sleep(5)
            except Exception as e:
                raise Exception(f"Error scraping page {page_number}: {e}")

        self.driver.quit()
        logging.info(f"Scraping completed. Extracted {len(self.data)} records.")

    def get_data_as_dataframe(self):
        """Convert collected data into a Pandas DataFrame."""
        return pd.DataFrame(self.data)

    def save_data(self, raw_dest_path):
        """Save scraped data to a CSV file."""
        save_to_csv(self.data, raw_dest_path)


class SaroutyScraperException(Exception):
    pass
