FROM python:3.11-slim

WORKDIR /app

# Instalamos solo lo necesario para PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de tu código
COPY . .

# Creamos la carpeta de subidas
RUN mkdir -p static/uploads

EXPOSE 5000

# Comando para arrancar la app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "hello:app"]