import pickle

from sklearn.metrics.pairwise import cosine_similarity
from src.features.preprocessor import column_transformer
from src.data.make_dataset import read_csv


try:
    raw_data_path = r".../data/processed/processed_data.csv"
    data = read_csv(file_path=raw_data_path)

    if data is not None:
        try:
            transformed_data = column_transformer.fit_transform(data).toarray()

        except Exception as e:
                    print(f"An error occurred during data transformation: {e}")

        try:
            similarity = cosine_similarity(transformed_data)
            # measuring distance with each vechors

        except Exception as e:
            print(f"An error occurred while calculating cosine similarity: {e}")

        try:
            with open('similarity.pkl', 'wb') as file:
                pickle.dump(similarity, file)
        except Exception as e:
                    print(f"An error occurred while saving the similarity matrix: {e}")
                    
except Exception as e:
    print(f"An unexpected error occurred: {e}")