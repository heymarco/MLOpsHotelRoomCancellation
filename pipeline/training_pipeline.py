from sklearn.ensemble import RandomForestClassifier

from config.paths_config import CONFIG_PATH, TRAIN_FILEPATH, TEST_FILEPATH, PROCESSED_DIR, PROCESSED_TRAIN_DATA_PATH, \
    PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml

if __name__ == '__main__':
    # Data ingestion
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()

    # Data preprocessing
    processor = DataProcessor(TRAIN_FILEPATH, TEST_FILEPATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()

    # Model training
    pipeline = ModelTraining(estimator_class=RandomForestClassifier,
                             train_path=PROCESSED_TRAIN_DATA_PATH,
                             test_path=PROCESSED_TEST_DATA_PATH,
                             model_output_path=MODEL_OUTPUT_PATH,
                             config_path=CONFIG_PATH)
    pipeline.run()
