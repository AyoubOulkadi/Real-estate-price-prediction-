import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def extract_property_data(driver, url_template, page_number):
    logging.info("Start Scraping Data...")

    url_scrapped = url_template.format(page_number=page_number)
    logging.info("Scraping from URL: %s", url_scrapped)

    driver.get(url_scrapped)
    time.sleep(10)

    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-intro__title"))
        )
    except TimeoutException as e:
        logging.error(f"Timeout while loading page {page_number}: {str(e)}", exc_info=True)
        return []

    try:
        articles = driver.find_elements(By.CSS_SELECTOR, '.card-intro__title')
        prices = driver.find_elements(By.CSS_SELECTOR, '.card-intro__price')
        locations = driver.find_elements(By.CSS_SELECTOR, '.card-specifications__location')
        types = driver.find_elements(By.CSS_SELECTOR, '.card-intro__type')
        categories = driver.find_elements(By.CSS_SELECTOR, '.card-specifications__amenities')

        properties = []
        for article, price, location, type_, category in zip(articles, prices, locations, types, categories):
            properties.append({
                "Scraped_URL": url_scrapped,
                "Article": article.text.strip(),
                "Price": price.text.strip(),
                "Location": location.text.strip(),
                "Type": type_.text.strip(),
                "Category": category.text.strip()
            })

        logging.info(f"Extracted {len(properties)} records from page {page_number}.")
        return properties
    except Exception as e:
        logging.error(f"Error extracting data on page {page_number}: {e}", exc_info=True)
        return []