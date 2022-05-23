FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
RUN pip install poetry
ENV PYTHONUNBUFFERED 1
ADD python-api/pyproject.toml /app
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt
ADD python-api /app
