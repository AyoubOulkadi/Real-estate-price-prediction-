from sqlalchemy import text
from config.utils import engine, databases, base_path, categories, subfolder
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class SaroutyIngestion:
    @staticmethod
    def create_databases(engine, databases):
        with engine.connect() as conn:
            for db in databases:
                result = conn.execute(text(f"SHOW DATABASES LIKE '{db}'"))
                if result.fetchone() is None:
                    conn.execute(text(f"CREATE DATABASE {db}"))
                else:
                    logging.info(f"Database {db} already exists.")

    @staticmethod
    def ingest_data(engine, base_path, categories, subfolder):
        with engine.connect() as conn:
            for category in categories:
                folder_path = os.path.join(base_path, category, subfolder)
                if not os.path.exists(folder_path):
                    logging.info(f"Folder does not exist: {folder_path}")
                    continue

                for filename in os.listdir(folder_path):
                    if filename.endswith(".csv"):
                        file_path = os.path.join(folder_path, filename)
                        df = pd.read_csv(file_path)

                        df.columns = df.columns.str.strip()

                        df.rename(columns={
                            'scraped_url': 'Scraped_URL',
                            'article': 'Article',
                            'price': 'Price',
                            'type': 'Type',
                            'date': 'date',
                            'bedrooms': 'Bedrooms',
                            'bathrooms': 'Bathrooms',
                            'surface': 'Surface',
                            'neighborhood': 'Neighborhood',
                            'city': 'City'
                        }, inplace=True)

                        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
                        df['Bedrooms'] = pd.to_numeric(df['Bedrooms'], errors='coerce')
                        df['Bathrooms'] = pd.to_numeric(df['Bathrooms'], errors='coerce')
                        df['Surface'] = pd.to_numeric(df['Surface'], errors='coerce')
                        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

                        db_name = f"{category}_db"
                        table_name = f"{category}_table"
                        conn.execute(text(f"USE {db_name}"))

                        # Create table with Article as unique field
                        conn.execute(text(f"""
                            CREATE TABLE IF NOT EXISTS {table_name} (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                Scraped_URL VARCHAR(255),
                                Article VARCHAR(255),
                                Price FLOAT,
                                Type VARCHAR(100),
                                date DATE,
                                Bedrooms INT,
                                Bathrooms INT,
                                Surface FLOAT,
                                Neighborhood VARCHAR(255),
                                City VARCHAR(100)
                            )
                        """))

                        # Fetch existing articles
                        existing_articles = conn.execute(text(f"SELECT Article FROM {table_name}")).fetchall()
                        existing_article_set = set(row[0] for row in existing_articles)

                        # Keep only new articles
                        new_df = df[~df['Article'].isin(existing_article_set)]

                        if not new_df.empty:
                            insert_query = text(f"""
                                INSERT INTO {table_name} (
                                    Scraped_URL, Article, Price, Type, date,
                                    Bedrooms, Bathrooms, Surface, Neighborhood, City
                                ) VALUES (
                                    :Scraped_URL, :Article, :Price, :Type, :date,
                                    :Bedrooms, :Bathrooms, :Surface, :Neighborhood, :City
                                )
                            """)
                            conn.execute(insert_query, new_df.to_dict(orient="records"))
                            logging.info(
                                f"Ingested {len(new_df)} new records from {file_path} into {db_name}.{table_name}")
                        else:
                            logging.info(f"No new data found in {file_path}. Skipping ingestion.")


def create_databases():
    SaroutyIngestion.create_databases(engine, databases)


def ingest_data():
    SaroutyIngestion.ingest_data(engine, base_path, categories, subfolder)
create_databases()
ingest_data()