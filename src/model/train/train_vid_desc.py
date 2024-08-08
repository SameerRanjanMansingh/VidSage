import numpy as np
import pickle

from sklearn.cluster import AffinityPropagation
from sentence_transformers import SentenceTransformer, util
from collections import Counter

from src.data.make_dataset import read_csv


try:
    model_name = 'paraphrase-MiniLM-L6-v2'
    model = SentenceTransformer(model_name)
except Exception as e:
    print(f"An error occurred while loading the model: {e}")

try:
    raw_data_path = r".../data/processed/description_data.csv"
    data = read_csv(file_path=raw_data_path)
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e} - Please check if the file path is correct.")
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")

try:
    train_embeddings = model.encode(data)
    train_embeddings = np.array(train_embeddings, dtype=np.float64)
except Exception as e:
    print(f"An error occurred while encoding the data: {e}")

try:
    affinity = AffinityPropagation(random_state=42)
    affinity.fit(train_embeddings)
except Exception as e:
    print(f"An error occurred during clustering: {e}")

try:
    with open('affinity.pkl', 'wb') as file:
        pickle.dump(affinity, file)
except Exception as e:
    print(f"An error occurred while saving the model: {e}")