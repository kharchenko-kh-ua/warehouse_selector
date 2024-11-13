# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY Pipfile* ./
RUN apt update -y && apt install libpq-dev gcc python3-dev -y && pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --system --dev

COPY . .
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
