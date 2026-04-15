FROM python:3.11-slim

WORKDIR /app

# Instalamos dependencias de sistema (Agregamos curl para el Healthcheck)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descarga de datos NLTK
RUN python -m nltk.downloader punkt punkt_tab stopwords averaged_perceptron_tagger wordnet

COPY . .
RUN mkdir -p static/uploadsS

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "hello:app"]