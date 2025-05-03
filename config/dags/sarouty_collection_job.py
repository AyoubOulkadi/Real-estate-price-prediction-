import schedule
import time
import subprocess
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_sales():
    logging.info(" Lancement du scraper Sales...")
    subprocess.run([
        "python", "C:\datalake\Real-estate-price-prediction\src\data_collection\main_collection.py",
        "--source", "Sales",
        "--param",
        "{\"url_sales_template\": \"https://www.sarouty.ma/acheter/proprietes-a-vendre.html?page={page_number}\", \"Sales_pages\": 2, \"sales_filename\": \"daily_sarouty_sales.csv\", \"base_raw_data_path\": \"C:\\\\datalake\\\\Real-estate-price-prediction\\\\Data\\\\raw_data\", \"dest_path_sales_path\": \"C:\\\\datalake\\\\Real-estate-price-prediction\\\\Data\\\\raw_data\\\\sales\\\\daily_data\"}"
    ])
    logging.info(" Sales terminé.\n")


def run_rent():
    logging.info(" Lancement du scraper Rent...")
    subprocess.run([
        "python", "C:\datalake\Real-estate-price-prediction\src\data_collection\main_collection.py",
        "--source", "Rent",
        "--param",
        "{\"url_rent_template\": \"https://www.sarouty.ma/fr/recherche?c=2&fu=0&ob=mr&page={page_number}&rp=m\", \"rent_filename\": \"daily_sarouty_rent.csv\", \"rent_pages\": 2, \"dest_path_rent_path\": \"C:\\\\datalake\\\\Real-estate-price-prediction\\\\Data\\\\raw_data\\\\rent\\\\daily_data\"}"
    ])
    logging.info(" Rent terminé.\n")


schedule.every().day.at("09:00").do(run_sales)
schedule.every().day.at("09:00").do(run_rent)

logging.info("Cron script en cours...")

while True:
    schedule.run_pending()
    time.sleep(60)
