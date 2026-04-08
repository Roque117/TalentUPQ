FROM python:3.11-slim

WORKDIR /app

# Instalamos dependencias de sistema para Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- NUEVA LÍNEA CRÍTICA PARA NLTK ---
# Esto descarga los datos que tu código va a buscar al arrancar
RUN python -m nltk.downloader punkt punkt_tab stopwords averaged_perceptron_tagger wordnet

COPY . .
RUN mkdir -p static/uploads

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "hello:app"]