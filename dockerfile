# builder
FROM python:3.11-slim as builder

WORKDIR /app

# dependencias de compilación
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Instalar dependencias en un directorio temporal
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

#runtime
FROM python:3.11-slim

WORKDIR /app

# Copiar solo lo necesario del builder
COPY --from=builder /install /usr/local
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
