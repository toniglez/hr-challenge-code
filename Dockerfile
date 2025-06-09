FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api ./api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
