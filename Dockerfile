FROM python:3.13-slim

WORKDIR /app

# Instalar dependencias del sistema usando el repositorio de Debian 11 (compatible con 12)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc-dev \
    curl \
    gnupg2 \
    && mkdir -p /etc/apt/keyrings \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/config/debian/11/prod.list main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Crear directorio para uploads
RUN mkdir -p static/uploads

# Puerto de la API
EXPOSE 5000

# Comando para ejecutar la app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "hello:app"]