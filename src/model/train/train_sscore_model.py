import pickle

from sklearn.metrics.pairwise import cosine_similarity
from src.features.preprocessor import column_transformer
from src.data.make_dataset import read_csv

try:
    raw_data_path = r"data/processed/processed_data.csv"
    data = read_csv(file_path=raw_data_path)

    if data is not None:
        transformed_data = column_transformer.fit_transform(data).toarray()

        similarity = cosine_similarity(transformed_data)
        # measuring distance with each vectors

        with open('models/similarity.pkl', 'wb') as file:
            pickle.dump(similarity, file)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    raise
