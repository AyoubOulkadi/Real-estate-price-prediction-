import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def extract_property_data(driver, base_url, page_number):
    """Extract property data from a single page and return a list of dictionaries."""
    url = f"{base_url}{page_number}"
    driver.get(url)

    # Wait for all elements to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card-list.card-list--property"))
        )
    except Exception as TimeOutException:
        raise TimeOutException(f"Timeout while loading page {page_number}: {TimeOutException}")

    articles = driver.find_elements(By.CSS_SELECTOR, '.card-intro__title')
    prices = driver.find_elements(By.CSS_SELECTOR, '.card-intro__price')
    locations = driver.find_elements(By.CSS_SELECTOR, '.card-specifications__location')
    types = driver.find_elements(By.CSS_SELECTOR, '.card-intro__type')
    categories = driver.find_elements(By.CSS_SELECTOR, '.card-specifications__amenities')

    properties = []
    for article, price, location, type, category in zip(articles, prices, locations, types, categories):
        properties.append({
            "Article": article.text.strip(),
            "Price": price.text.strip(),
            "Location": location.text.strip(),
            "Type": type.text.strip(),
            "Category": category.text.strip()
        })

    return properties
