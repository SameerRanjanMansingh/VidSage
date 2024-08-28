FROM python:3.11.9-slim

WORKDIR /app

COPY flask_app/ /app/

COPY models/affinity.pkl /app/models/affinity.pkl

COPY models/similarity.pkl /app/models/similarity.pkl

COPY data/processed/description_data.csv /app/data/processed/description_data.csv

COPY data/processed/processed_data.csv /app/data/processed/processed_data.csv

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]