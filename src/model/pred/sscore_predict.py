import pandas as pd
import logging

from logger_module.my_logger import setup_custom_logger



logger = setup_custom_logger("my_app", log_level=logging.INFO, log_file="model.log")



def recommend(data: pd.DataFrame, video_id: str, similarity: list) -> list:
    """
    Recommends videos based on similarity to a given video_id.
    
    Parameters:
    data (pd.DataFrame): Dataframe containing video data.
    video_id (str): ID of the video to base recommendations on.
    similarity (list): List of similarity scores.
    
    Returns:
    list: List of recommended video indices.
    """
    try:
        # Get all indices of the given video_id
        indices = data[data['video_id'] == video_id].index.tolist()
        
        # Collect distances for all indices
        all_distances = []
        for index in indices:
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            all_distances.extend(distances)
        
        # Remove duplicates and sort by distance
        unique_distances = list(dict(sorted(all_distances, key=lambda x: x[1], reverse=True)).items())
        
        # Get the top 2 distances for the same video_id
        top_2_same_video = [dist for dist in unique_distances if data.iloc[dist[0]].video_id == video_id][:2]
        
        # Get the remaining items up to a total of 5 recommendations
        remaining_items = [dist for dist in unique_distances if data.iloc[dist[0]].video_id != video_id][:5 - len(top_2_same_video)]
        
        # Combine the results
        recommendations = top_2_same_video + remaining_items
        
        # Get the video_id of the second most similar video
        second_video_id = data.iloc[unique_distances[1][0]].video_id
        
        # Get all indices of the second most similar video_id
        second_indices = data[data['video_id'] == second_video_id].index.tolist()
        
        # Collect distances for all indices of the second most similar video_id
        second_all_distances = []
        for index in second_indices:
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            second_all_distances.extend(distances)
        
        # Remove duplicates and sort by distance
        second_unique_distances = list(dict(sorted(second_all_distances, key=lambda x: x[1], reverse=True)).items())
        
        # Get the top 2 distances for the second most similar video_id
        top_2_second_video = [dist for dist in second_unique_distances if data.iloc[dist[0]].video_id == second_video_id][:2]
        
        # Get the remaining items up to a total of 5 recommendations
        remaining_items_second = [dist for dist in second_unique_distances if data.iloc[dist[0]].video_id != second_video_id][:5 - len(top_2_second_video)]
        
        # Combine the results
        final_recommendations = recommendations + top_2_second_video + remaining_items_second[:1]
        
        # Ensure the final recommendations list contains exactly 5 items
        final_recommendations = final_recommendations[:5]
        
        return final_recommendations
    
    except KeyError as e:
        print(f"KeyError: {e} - Please check if the column names are correct.")
    except Exception as e:
        logger.critical(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

