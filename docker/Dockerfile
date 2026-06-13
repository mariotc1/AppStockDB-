FROM python:3.11-slim

WORKDIR /app

# Deps del sistema necesarias para mysql-connector-python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Solo instala las dependencias de la API (imagen más pequeña que con requirements.txt completo)
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# Código de la API
COPY backend/ ./backend/

# Carpeta de uploads (fotos de perfil); se monta como volumen en producción
RUN mkdir -p uploads

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Desarrollo: un worker, recarga automática
# Producción: sobreescribir con CMD en docker-compose.prod.yml
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", \
     "--timeout", "120", "--access-logfile", "-", "api:app"]
