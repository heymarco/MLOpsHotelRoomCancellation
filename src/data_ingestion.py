import os
from dotenv import load_dotenv
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml


load_dotenv()
logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data ingestion started with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILEPATH)
            logger.info(f"Successfully downloaded CSV file to {RAW_FILEPATH}")
        except Exception as e:
            logger.error("Error while downloading CSV file")
            raise CustomException("Failed to download CSV file", e)

    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            data = pd.read_csv(RAW_FILEPATH)
            train_data, test_data = train_test_split(data, train_size=self.train_ratio, random_state=0)
            train_data.to_parquet(TRAIN_FILEPATH)
            test_data.to_parquet(TEST_FILEPATH)

            logger.info(f"Train data saved to {TRAIN_FILEPATH}")
            logger.info(f"Test data saved to {TEST_FILEPATH}")
        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException("Failed to split data", e)

    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion completed successfully")
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        finally:
            logger.info("Data ingestion completed")


if __name__ == '__main__':
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()

