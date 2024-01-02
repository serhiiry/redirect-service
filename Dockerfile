FROM --platform=linux/arm64 python:3.12-slim as builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev --without testing

COPY . /app

FROM --platform=linux/arm64 python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app /app

EXPOSE 80

ENV PATH="/usr/local/bin:$PATH" \
    PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
