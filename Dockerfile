FROM python:3.13-slim

WORKDIR /app

# Solo instalamos GCC y G++ por si alguna librería de Python lo necesita para compilar
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Crear directorios necesarios con permisos
RUN mkdir -p static/uploads /data

# Puerto de la API
EXPOSE 5000

# Comando para ejecutar la app
# Usamos gunicorn para producción, hello es el nombre de tu archivo y app es la variable de Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "hello:app"]