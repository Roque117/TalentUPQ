FROM python:3.13-slim

WORKDIR /app

# Paso 1: Instalar herramientas básicas de red y compilación
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    gcc \
    g++ \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Paso 2: Configurar el repositorio de Microsoft e instalar el driver ODBC
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Paso 3: Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Paso 4: Copiar el resto del código
COPY . .
RUN mkdir -p static/uploads

EXPOSE 5000

CMD ["python", "hello.py"]