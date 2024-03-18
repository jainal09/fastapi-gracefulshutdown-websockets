FROM python:3.12-slim

RUN pip install poetry

workdir /app
copy pyproject.toml .

copy poetry.lock /app/poetry.lock

Run poetry config virtualenvs.create false

Run poetry install --no-dev

workdir /app

copy . /app

EXPOSE 8000
entrypoint ["python", "main.py"]



