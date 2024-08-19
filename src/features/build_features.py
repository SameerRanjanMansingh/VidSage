import re


def initial_process(df):
    """
    Initial processing of the dataframe.
    
    Parameters:
    df (pd.DataFrame): Input dataframe.
    file_type (str): Type of the input file (default is 'csv').
    
    Returns:
    pd.DataFrame: Processed dataframe.
    """
    try:
        # Drop duplicate rows
        df = df.drop_duplicates(subset=['video_id'], keep='first', inplace=False)

        # Filter out rows where 'video_error_or_removed' is True
        df = df[df['video_error_or_removed'] == False]

        # Drop the 'video_error_or_removed' column
        df.drop(columns=["video_error_or_removed"], inplace=True)

        # Fill NaN values in 'description' column
        df.loc[df.description.isnull(), "description"] = "Information not available"

        return df

    except KeyError as e:
        print(f"KeyError: {e} - Please check if the column names are correct.")
    except Exception as e:
        print(f"An error occurred: {e}")


def text_cleaning(text):
    """
    Cleans the input text by removing hyperlinks, new lines, and commas.
    
    Parameters:
    text (str): Input text to be cleaned.
    
    Returns:
    str: Cleaned text.
    """
    try:
        # Remove hyperlinks that start with http://, https://, or www.
        cleaned_text = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove hyperlinks that have typical URL structure with domain and possibly a path
        cleaned_text = re.sub(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b(?!\S)', '', cleaned_text)

        # Removing new lines and commas
        cleaned_text = cleaned_text.replace('\\n', '').replace(',', '')

        return cleaned_text

    except Exception as e:
        print(f"An error occurred: {e}")


def add_new_feature(df):
    """
    Adds a new feature 'row_summary' to the dataframe, summarizing key information.
    
    Parameters:
    df (pd.DataFrame): Input dataframe.
    
    Returns:
    pd.DataFrame: Dataframe with the new 'row_summary' feature.
    """
    try:
        df["row_summary"] = df.apply(
            lambda row: f'''
            trending_date = {row["trending_date"]},
            publish_time = {row["publish_time"]},
            views = {row["views"]},
            likes = {row["likes"]},
            dislikes = {row["dislikes"]},
            comment_count = {row["comment_count"]},
            comments_disabled = {row["comments_disabled"]},
            ratings_disabled = {row["ratings_disabled"]},
            title = {row["title"]},
            channel_title = {row["channel_title"]},
            description = {row["description"]}''', axis=1
        ).apply(lambda x: x.replace('\n', ''))

        return df

    except KeyError as e:
        print(f"KeyError: {e} - Please check if the column names are correct.")
    except Exception as e:
        print(f"An error occurred: {e}")
