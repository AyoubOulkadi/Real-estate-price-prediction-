from src.data_collection.main_collection import SaroutyScraper

if __name__ == "__main__":
    scraper = SaroutyScraper(max_pages=20)
    scraper.scrape_all_pages()

    df = scraper.get_data_as_dataframe()
    print(df.head())  # Show first few rows

    scraper.save_data("sarouty_data.csv")
