FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
RUN pip install poetry
ENV PYTHONUNBUFFERED 1
ADD pyproject.toml /app
RUN poetry export -f requirements.txt --output requirements.txt --dev
RUN pip install -r requirements.txt
ADD . /app
