FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# CMD ["poetry", "run", "python", "botish/main.py"]