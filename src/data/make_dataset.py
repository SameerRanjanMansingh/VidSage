import pathlib
import pandas as pd
import logging

from src.features.build_features import initial_process, text_cleaning, add_new_feature
from logger_module.my_logger import setup_custom_logger

logger = setup_custom_logger("my_app", log_level=logging.INFO, log_file="model.log")


def read_csv(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a dataframe.
    
    Parameters:
    file_path (str): Path to the CSV file.
    
    Returns:
    pd.DataFrame: Dataframe containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as file_error:
        print(f"FileNotFoundError: {file_error} - Please check if the file path is correct.")
        raise

    except Exception as general_error:
        print(f"An error occurred: {general_error}")
        raise


def main(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the dataframe by cleaning text and applying initial processing.
    
    Parameters:
    df (pd.DataFrame): Input dataframe.
    
    Returns:
    pd.DataFrame: Processed dataframe.
    """
    try:
        df = initial_process(df)
        df["title"] = df["title"].apply(text_cleaning)
        df["tags"] = df["tags"].apply(text_cleaning)
        df["description"] = df["description"].apply(text_cleaning)

        df["title"] = df["title"].apply(lambda x: x.replace(" | ", " "))
        df["tags"] = df["tags"].apply(lambda x: x.replace("|", " ").replace('"', ''))

        return df
    except KeyError as error:
        print(f"KeyError: {error} - Please check if the column names are correct.")
        raise
    except Exception as error:
        print(f"An error occurred: {error}")
        raise


def description_data_process(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the dataframe to add a new feature and clean the 'row_summary' column.
    
    Parameters:
    df (pd.DataFrame): Input dataframe.
    
    Returns:
    pd.DataFrame: Dataframe with processed 'row_summary' feature.
    """
    try:
        df = add_new_feature(df)
        df["row_summary"] = df["row_summary"].apply(lambda x: x.replace("|", " ").replace('"', '').replace(" | ", " "))
        return df
    except KeyError as error:
        print(f"KeyError: {error} - Please check if the column names are correct.")
        raise
    except Exception as error:
        print(f"An error occurred: {error}")
        raise


def save_data(df: pd.DataFrame, file_name: str):
    """
    Saves the dataframe to a CSV file in the specified directory.
    
    Parameters:
    df (pd.DataFrame): Dataframe to be saved.
    file_name (str): Name of the output CSV file.
    """
    try:
        output_path = "data/processed/"
        pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path + file_name, index=False)
    except Exception as error:
        print(f"An error occurred: {error}")
        raise


if __name__ == '__main__':
    try:
        IN_raw_data_path = r"data/raw/INvideos.csv"
        # US_raw_data_path = r"data/raw/USvideos.csv"
        # GB_raw_data_path = r"data/raw/GBvideos.csv"

        IN_data = read_csv(file_path=IN_raw_data_path)
        # US_data = read_csv(file_path=US_raw_data_path)
        # GB_data = read_csv(file_path=GB_raw_data_path)

        IN = main(df=IN_data)
        # US = main(df=US_data)
        # GB = main(df=GB_data)


        '''
        data = pd.concat([IN, US, GB], axis=0)

        Use whole data for more robust performance
        I ignored these because of s3 bucket issue, file is too large, takes too long to training
        '''

        data=IN.iloc[:10000,:]
        
        save_data(df=data, file_name="processed_data.csv")

        description_data = description_data_process(df=data)
        save_data(df=description_data, file_name="description_data.csv")

        logger.info("Data cleaning completed")

    except Exception as e:
        print(f"An error occurred during execution: {e}")
        raise
