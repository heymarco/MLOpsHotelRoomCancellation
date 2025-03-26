import joblib
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.hyperparameters import *
from utils.common_functions import read_yaml, load_data

import mlflow
from mlflow import sklearn as mlfsklearn


logger = get_logger(__name__)


class ModelTraining:
    def __init__(self, estimator_class, train_path: str, test_path: str, model_output_path: str, config_path: str):
        self.estimator_class = estimator_class
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.hp_search_space = RF_SEARCH_SPACE
        self.random_search_params = RANDOM_SEARCH_PARAMS

        self.config = read_yaml(config_path)

    def _load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            target_column = self.config["data_processing"]["target_column"]
            X_train, y_train = train_df.drop(columns=target_column), train_df[target_column]
            X_test, y_test = test_df.drop(columns=target_column), test_df[target_column]

            logger.info("Data splitted successfully for model training")

            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error loading and splitting data {e}")
            raise CustomException("Failed to load and split data", e)

    def _train_model(self, X_train, y_train):
        try:
            logger.info(f"Initializing model {self.estimator_class.__name__}")
            rf = self.estimator_class(random_state=self.random_search_params["random_state"])
            rscv = RandomizedSearchCV(
                estimator=rf,
                param_distributions=self.hp_search_space,
                **self.random_search_params)

            logger.info("Starting hyperparameter tuning")
            rscv.fit(X_train, y_train)

            best_params = rscv.best_params_
            best_model = rscv.best_estimator_
            logger.info(f"Best parameters are {best_params}")

            return best_model
        except Exception as e:
            logger.error(f"Error training model {self.estimator_class.__name__} {e}")
            raise CustomException("Failed to train random forest", e)

    def _evaluate_model(self, model, X_test, y_test) -> dict:
        try:
            logger.info("Evaluating model")
            pred = model.predict(X_test)
            metrics = {"Accuracy": accuracy_score, "Recall": recall_score,
                       "Precision": precision_score, "F1": f1_score}

            achieved_metrics = {}
            for metric_name, metric_func in metrics.items():
                score = metric_func(y_test, pred)
                achieved_metrics[metric_name] = score

            logger.info(f"Metrics are {achieved_metrics}")
            return achieved_metrics
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("Failed to evaluate model", e)

    def _save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info("Saving the model")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error while saving model {e}")
            raise CustomException("Failed to save model", e)

    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting MLFlow experiment")
                logger.info("Starting model training pipeline")

                X_train, y_train, X_test, y_test = self._load_and_split_data()
                model = self._train_model(X_train, y_train)
                metrics = self._evaluate_model(model, X_test, y_test)
                self._save_model(model)

                self._log_to_mlflow(metrics, model)

                logger.info("Successfully finished model training pipeline")
        except Exception as e:
            logger.error(f"Error in model training pipeline {e}")
            raise CustomException("Failed to execute model training pipeline", e)

    def _log_to_mlflow(self, metrics, model):
        try:
            logger.info("Logging training and testing data in MLFlow")
            mlflow.log_artifact(self.train_path, artifact_path="datasets")
            mlflow.log_artifact(self.test_path, artifact_path="datasets")
            logger.info("Logging model in MLFlow")
            logger.info("Logging model metrics in MLFlow")
            mlflow.log_metrics(metrics)
            mlflow.log_artifact(MODEL_OUTPUT_PATH)
            logger.info("Logging model params in MLFlow")
            mlflow.log_params(model.get_params())
        except Exception as e:
            logger.error(f"Error while logging to MLFlow {e}")
            raise CustomException("Failed to log to MLFlow", e)


if __name__ == '__main__':
    pipeline = ModelTraining(estimator_class=RandomForestClassifier,
                             train_path=PROCESSED_TRAIN_DATA_PATH,
                             test_path=PROCESSED_TEST_DATA_PATH,
                             model_output_path=MODEL_OUTPUT_PATH,
                             config_path=CONFIG_PATH)
    pipeline.run()
