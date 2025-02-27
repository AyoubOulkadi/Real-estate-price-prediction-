import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def save_to_csv(data,raw_dest_path):
    """Save scraped data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(raw_dest_path, index=False)
    logging.info(f"Data saved to {raw_dest_path}")
