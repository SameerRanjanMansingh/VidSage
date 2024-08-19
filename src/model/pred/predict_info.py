import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW


from transformers import pipeline
paragraph = """
The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet at least once.
It is often used to test typewriters and keyboards. The sentence is known for its use in pangrams.
"""
qa_pipeline = pipeline("question-answering")

def answer_question(question, context):
    result = qa_pipeline(question=question, context=context)
    return result['answer']

print(answer_question(["What are languages used in this video?"], paragraph))