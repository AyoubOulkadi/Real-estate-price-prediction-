import time
import logging
import pandas as pd
import os

from src.data_collection.extract_property_data import extract_property_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class SaroutyScraper:
    @staticmethod
    def scrape_all_pages(driver, pages, url):
        data = []

        for page_number in range(1, pages + 1):
            try:
                logging.info(f"Scraping page {page_number}...")
                page_data = extract_property_data(driver, url, page_number)
                data.extend(page_data)
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error scraping page {page_number}: {e}")
                break

        driver.quit()
        logging.info(f"Scraping completed. Extracted {len(data)} records.")

        return data

    @staticmethod
    def save_data(data, raw_dest_path, filename):
        if not data:
            logging.warning("No data to save.")
            return
        current_date = pd.to_datetime("today").date()
        data['date'] = current_date

        year = current_date.year
        month = str(current_date.month).zfill(2)
        day = str(current_date.day).zfill(2)
        raw_dest_path = os.path.abspath(raw_dest_path)

        partition_folder = os.path.join(raw_dest_path, f"year={year}", f"month={month}", f"day={day}")
        os.makedirs(partition_folder, exist_ok=True)

        partition_file_path = os.path.join(partition_folder, filename)

        data.to_csv(partition_file_path, index=False)
        logging.info(f"Saved data for {current_date} to {partition_file_path}")


class SaroutyScraperException(Exception):
    pass
