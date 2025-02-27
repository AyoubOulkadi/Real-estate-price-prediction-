from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """Setup and return the Chrome WebDriver."""
    options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("start-maximized")
    options.add_argument("--disable-default-apps")
    options.add_argument("disable-infobars")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
