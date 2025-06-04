# -------- Builder Stage --------
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apk add --no-cache gcc musl-dev curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install --no-deps -r requirements.txt

# -------- Runtime Stage --------
FROM python:3.12-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH=/usr/local/lib/python3.12/site-packages

WORKDIR /app

COPY --from=builder /install /usr/local

COPY alembic.ini .
COPY alembic ./alembic

COPY app ./app
COPY scripts ./scripts

RUN chmod +x scripts/prestart.sh

EXPOSE 8000

CMD ["./scripts/prestart.sh"]