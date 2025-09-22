# Multi-stage build for smaller image
FROM python:3.11-slim AS builder
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential locales --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
RUN addgroup --system appgroup && adduser --system --ingroup appgroup --disabled-password appuser
WORKDIR /app

# Instalar locales y configurar UTF-8
RUN apt-get update && apt-get install -y locales --no-install-recommends \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Copiar dependencias del builder
COPY --from=builder /usr/local /usr/local

COPY . /app
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8050
CMD ["gunicorn", "cinehub_project.wsgi:application", "--bind", "0.0.0.0:8050", "--workers", "3", "--timeout", "120"]
