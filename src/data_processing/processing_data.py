import pandas as pd
import os
from glob import glob
from config.utils import rent_base_path, sales_base_path, rent_output, sales_output, historical_rent_path, \
    historical_sales_path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class SaroutyProcessing:
    @staticmethod
    def process_data(filepath: str) -> pd.DataFrame:
        df = pd.read_csv(filepath)

        df[['Bedrooms', 'Bathrooms', 'Surface']] = df["Category"].apply(
            lambda x: pd.Series(str(x).split("\n"))
        )

        df = df.dropna()

        for col in ['Bedrooms', 'Bathrooms', 'Surface', 'Price']:
            df[col] = df[col].str.replace(r'[^\d]', '', regex=True)
            df = df[df[col] != '']
            df[col] = df[col].astype(int)

        df[['Neighborhood', 'City']] = df['Location'].str.split(', ', 1, expand=True)
        df = df.drop(["Location", "Category"], axis=1)

        return df

    @staticmethod
    def save_df(df: pd.DataFrame, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)

    @staticmethod
    def find_latest_file(base_path: str, pattern: str = "*.csv") -> str:
        search_path = os.path.join(base_path, '**', pattern)
        files = glob(search_path, recursive=True)
        if not files:
            raise FileNotFoundError(f"No CSV files found in {base_path}")
        latest_file = max(files, key=os.path.getmtime)
        return latest_file

    @staticmethod
    def merge_data(daily_path: str, historical_path: str) -> pd.DataFrame:
        historical_df = pd.read_csv(historical_path)
        daily_df = pd.read_csv(daily_path)
        merged_df = pd.concat([historical_df, daily_df], ignore_index=True)
        merged_df = merged_df.drop_duplicates()
        return merged_df


def run_processing_pipeline():
    rent_csv = SaroutyProcessing.find_latest_file(rent_base_path)
    sales_csv = SaroutyProcessing.find_latest_file(sales_base_path)

    processed_rent_df = SaroutyProcessing.process_data(rent_csv)
    processed_sales_df = SaroutyProcessing.process_data(sales_csv)

    SaroutyProcessing.save_df(processed_rent_df, rent_output)
    SaroutyProcessing.save_df(processed_sales_df, sales_output)

    logging.info(f"Processed and saved Daily Rent Output: {rent_output}")
    logging.info(f"Processed and saved Daily Sales Output: {sales_output}")

    merged_rent = SaroutyProcessing.merge_data(rent_output, historical_rent_path)
    SaroutyProcessing.save_df(merged_rent, historical_rent_path)
    logging.info(f"Merged rent data with historical.")

    merged_sales = SaroutyProcessing.merge_data(sales_output, historical_sales_path)
    SaroutyProcessing.save_df(merged_sales, historical_sales_path)
    logging.info(f"Merged sales data with historical.")
run_processing_pipeline()