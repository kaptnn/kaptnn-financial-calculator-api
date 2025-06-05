# -------- Builder Stage --------
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache gcc musl-dev libffi-dev curl

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-deps -r requirements.txt


# -------- Runtime Stage --------
FROM python:3.12-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN apk add --no-cache bash curl libffi

WORKDIR /app

COPY --from=builder /install /usr/local

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app
COPY scripts ./scripts

RUN find ./scripts -type f -name "*.sh" -exec sed -i 's/\r$//' {} \;
RUN chmod +x scripts/prestart.sh

EXPOSE 8000

CMD ["bash", "./scripts/prestart.sh"]