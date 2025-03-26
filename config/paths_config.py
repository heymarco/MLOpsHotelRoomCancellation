import os

# DATA INGESTION
RAW_DIR = os.path.join("artifacts", "raw")
RAW_FILEPATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILEPATH = os.path.join(RAW_DIR, "train.parquet")
TEST_FILEPATH = os.path.join(RAW_DIR, "test.parquet")

CONFIG_PATH = os.path.join("config", "config.yaml")


# DATA PROCESSING
PROCESSED_DIR = os.path.join("artifacts", "processed")
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.parquet")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.parquet")
