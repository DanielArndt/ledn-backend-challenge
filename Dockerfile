FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
RUN pip install poetry
ENV PYTHONUNBUFFERED 1
ADD python-api/pyproject.toml /app
RUN poetry install
ADD python-api /app
