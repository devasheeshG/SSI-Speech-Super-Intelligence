FROM python:3.10-slim AS base
WORKDIR /app

# Install dependencies
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy source code
COPY . /app

# Run the application
