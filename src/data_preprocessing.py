import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.preprocessing import LabelEncoder


logger = get_logger(__name__)


class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)["data_processing"]

        os.makedirs(processed_dir, exist_ok=True)

    def process(self):
        try:
            logger.info(f"Loading data from {self.train_path} and {self.test_path}")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df, test_df = self._preprocess_data(train_df, test_df)
            self._save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self._save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data preprocessing completed successfully")

        except Exception as e:
            logger.error(f"Error during data preprocessing {e}")
            raise CustomException("Error during data preprocessing", e)

    def _preprocess_data(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        try:
            logger.info("Starting data preprocessing")
            self._drop_columns(train_df)
            self._drop_columns(test_df)
            self._encode_categorical(train_df, test_df)
            self._reduce_skewness(train_df)
            self._reduce_skewness(test_df)
            return train_df, test_df

        except Exception as e:
            logger.error(f"Error during preprocessing step {e}")
            raise CustomException("Error while preprocessing data", e)

    def _reduce_skewness(self, df):
        logger.info("Reducing skew in data:")
        num_cols = self.config["numerical_columns"]
        skew = df[num_cols].skew()
        skew_threshold = self.config["skew_threshold"]
        for col in skew.index[skew > skew_threshold]:
            df[col] = np.log1p(df[col])

    def _encode_categorical(self, train_df, test_df):
        logger.info("Encode labels")
        cat_cols = self.config["categorical_columns"]
        mappings = {}
        label_encoder = LabelEncoder()
        for col in cat_cols:
            train_df[col] = label_encoder.fit_transform(train_df[col])
            test_df[col] = label_encoder.transform(test_df[col])
            mappings[col] = {
                label: code for label, code
                in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))
            }
        logger.info("Label mappings are:")
        for col, mapping in mappings.items():
            logger.info(f"{col}: {mapping}")

    def _drop_columns(self, df):
        logger.info("Dropping columns")
        df.drop(self.config["dropped_columns"], axis=1, inplace=True)

    def _save_data(self, df: pd.DataFrame, filepath: str):
        try:
            logger.info(f"Saving data under {filepath}")
            _, ext = os.path.splitext(filepath)
            if ext == ".parquet":
                df.to_parquet(filepath, index=False)
            elif ext == ".csv":
                df.to_csv(filepath, index=False)
            else:
                raise NotImplementedError
        except Exception as e:
            logger.error(f"Error saving data at {filepath} {e}")
            raise CustomException(f"Error saving data", e)


if __name__ == '__main__':
    processor = DataProcessor(TRAIN_FILEPATH, TEST_FILEPATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()