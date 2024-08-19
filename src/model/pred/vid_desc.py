import joblib
from sentence_transformers import SentenceTransformer, util
from collections import Counter

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW

import numpy as np


# model_name = 'paraphrase-MiniLM-L6-v2'
# model = SentenceTransformer(model_name)

# train_embeddings = model.encode(X)
# train_embeddings = np.array(train_embeddings, dtype=np.float64)  # Ensure dtype is float64




# affinity = joblib.load('models/affinity.pkl')


# cluster_labels = affinity.labels_


# query_sentence = "Stylish Star Allu Arjun @ ChaySam Wedding Reception"


def search_result(query, model, affinity, labels, data):

    query_embedding = model.encode(query)
    nearest_cluster = affinity.predict([query_embedding])[0]

    # Retrieve sentences within the nearest cluster
    cluster_sentences = [data.iloc[i].row_summary for i in range(data.shape[0]) if labels[i] == nearest_cluster]


    # Count sentence frequencies
    sentence_frequencies = Counter(cluster_sentences).most_common(5)

    most_frequent_sentences = [i[0] for i in sentence_frequencies]

    result = [
        data[data.row_summary == most_frequent_sentences[i]].video_id.values[0] for i in range(len(most_frequent_sentences))
    ]
    
    return result


