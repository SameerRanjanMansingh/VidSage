import pickle

from flask import Flask, render_template, request, session
from sentence_transformers import SentenceTransformer
from transformers import pipeline

from src.data.make_dataset import read_csv
from src.model.pred.sscore_predict import get_similar_videos
from src.model.pred.vid_desc import search_result

import secrets


model_name = 'paraphrase-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

description_data = read_csv(file_path=r"data/processed/description_data.csv")
processed_data = read_csv(file_path=r"data/processed/processed_data.csv")

affinity = pickle.load(open('models/affinity.pkl', 'rb'))

cluster_labels = affinity.labels_

similarity = pickle.load(open('models/similarity.pkl', 'rb'))

qa_pipeline = pipeline("question-answering")


def answer_question(question, context):
    result = qa_pipeline(question=question, context=context)
    return result['answer']


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)


@app.route('/')
def home():
    search_details = session.get('search_details', None)  # Retrieve search_details from session
    query_answer = session.get('query_answer', None)
    selected_video_id = session.get('selected_video_id', None)
    thumbnail = session.get('thumbnail', None)
    recomendation = session.get('recomendation', None)

    return render_template('index.html', search_details=search_details, query_answer=query_answer,
                           selected_video_id=selected_video_id, thumbnail=thumbnail, recomendation=recomendation)


@app.route('/search', methods=['POST'])
def search():
    query = request.form['search_query']

    videoid = search_result(query=query, model=model, affinity=affinity, labels=cluster_labels, data=description_data)

    details = {videoid[i]: {
        'thumbnail_link': description_data[description_data.video_id == videoid[i]].thumbnail_link.values[0],
        'title': description_data[description_data.video_id == videoid[i]].title.values[0]} for i in
        range(len(videoid))}

    # return render_template('index.html', thumbnails=thumbnails)
    search_details = session.get('search_details', {})
    update_count = session.get('update_count', 0)

    # Update the thumbnails dictionary with the new data
    search_details.update(details)

    # Increment the update count
    update_count += 1

    # Check if the update count has reached 3
    if update_count >= 3:
        search_details = {}  # Clear the thumbnails cache
        update_count = 0  # Reset the update count

        query_answer = session.get('query_answer', None)
        selected_video_id = session.get('selected_video_id', None)
        thumbnail = session.get('thumbnail', None)
        recomendation = session.get('recomendation', None)

    # Store the updated thumbnails and update count back in the session
    session['search_details'] = search_details
    session['update_count'] = update_count

    query_answer = session.get('query_answer')
    selected_video_id = session.get('selected_video_id')
    thumbnail = session.get('thumbnail')
    recomendation = session.get('recomendation')

    return render_template('index.html', search_details=search_details, query_answer=query_answer,
                           selected_video_id=selected_video_id, thumbnail=thumbnail, recomendation=recomendation)


@app.route('/query', methods=['POST'])
def query():
    selected_video_id = request.form.getlist('selected_video_id[]')

    if len(list(selected_video_id)) > 1:
        return recomend(video_list=selected_video_id)
    else:
        thumbnail = description_data[description_data['video_id'] == selected_video_id[0]].thumbnail_link.values[0]
        session['thumbnail'] = thumbnail
        session['selected_video_id'] = selected_video_id

        search_details = session.get('search_details')
        query_answer = session.get('query_answer')
        recomendation = session.get('recomendation')

        return render_template('index.html', search_details=search_details, query_answer=query_answer,
                               selected_video_id=selected_video_id, thumbnail=thumbnail, recomendation=recomendation)


@app.route('/video_query', methods=['POST'])
def video_query():
    query = request.form['query']

    selected_video_id = session.get('selected_video_id')

    context = description_data[description_data['video_id'] == selected_video_id[0]].row_summary.values[0]

    answer = answer_question(question=[query], context=[context])

    session['query_answer'] = answer

    search_details = session.get('search_details')
    selected_video_id = session.get('selected_video_id')
    thumbnail = session.get('thumbnail')
    recomendation = session.get('recomendation')

    return render_template('index.html', search_details=search_details, query_answer=answer,
                           selected_video_id=selected_video_id, thumbnail=thumbnail, recomendation=recomendation)


# @app.route('/like', methods=['POST'])
def recomend(video_list):
    recomendation = get_similar_videos(data=processed_data, similarity=similarity, video_id=list(video_list))

    search_details = session.get('search_details')
    query_answer = session.get('query_answer')
    selected_video_id = session.get('selected_video_id')
    thumbnail = session.get('thumbnail')

    return render_template('index.html', search_details=search_details, query_answer=query_answer,
                           selected_video_id=selected_video_id, thumbnail=thumbnail, recomendation=recomendation)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
