FROM python:3.7-slim
# если убрать эту строку то контейнер на локальной машине не собирается
# Error: pg_config executable not found.
RUN apt-get update && apt-get -y install libpq-dev gcc
WORKDIR /app
COPY requirements.txt .
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]