from src.data_collection.main_collection import SaroutyScraper

if __name__ == "__main__":
    scraper = SaroutyScraper(max_pages=20)
    scraper.scrape_all_pages()

    df = scraper.get_data_as_dataframe()

    scraper.save_data(r"C:\datalake\Real-estate-price-prediction\Data\Raw_Data\raw_sarouty_data.csv")
