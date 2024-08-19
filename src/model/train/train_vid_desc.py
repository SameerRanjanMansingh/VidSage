from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
from sklearn.cluster import AffinityPropagation
from src.data.make_dataset import read_csv


# Load the model
model_name = 'paraphrase-MiniLM-L6-v2'
model = SentenceTransformer(model_name)



try:
    # Read the CSV file
    raw_data_path = r"data/processed/description_data.csv"
    data = read_csv(file_path=raw_data_path)

    # Encode the data
    train_embeddings = model.encode(data['row_summary'].tolist())
    train_embeddings = np.array(train_embeddings, dtype=np.float64)

    # Perform clustering
    affinity = AffinityPropagation(random_state=42)
    affinity.fit(train_embeddings)

    # Save the model
    with open('models/affinity.pkl', 'wb') as file:
        pickle.dump(affinity, file)

except FileNotFoundError as e:
    print(f"FileNotFoundError: {e} - Please check if the file path is correct.")
except Exception as e:
    print(f"An error occurred: {e}")
