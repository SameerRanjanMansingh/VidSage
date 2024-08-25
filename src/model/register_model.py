# register model

import pickle
import mlflow
import logging
import os

import logging

from logger_module.my_logger import setup_custom_logger

logger = setup_custom_logger("my_app", log_level=logging.INFO, log_file="model.log")


# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("DAGSHUB_PAT")
if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "SameerRanjanMansingh"
repo_name = "VidSage"

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')


def load_model_info(file_path: str) -> dict:
    """Load the model info from a pickle file."""
    try:
        with open(file_path, 'r') as file:
            model_info = pickle.load(file)
        logger.debug('Model info loaded from ', file_path)
        return model_info
    except FileNotFoundError:
        logger.error('File not found: ', file_path)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the model info: ', e)
        raise

def register_model(model_name: str, model_info: dict):
    """Register the model to the MLflow Model Registry."""
    try:
        model_uri = f"runs:/{model_info['run_id']}/{model_info['model_path']}"
        
        # Register the model
        model_version = mlflow.register_model(model_uri, model_name)
        
        # Transition the model to "Staging" stage
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Staging"
        )
        
        logger.debug(f'Model {model_name} version {model_version.version} registered and transitioned to Staging.')
    except Exception as e:
        logger.error('Error during model registration: ', e)
        raise

def main():
    try:
        affinity_model = 'models/affinity.pkl'
        similarity = 'models/similarity.pkl'

        affinity_model_info = load_model_info(affinity_model)
        similarity_model_info = load_model_info(similarity)
        
        register_model(affinity_model_info, "affinity_model")
        register_model(similarity_model_info, "similarity")

    except Exception as e:
        logger.error('Failed to complete the model registration process: ', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
