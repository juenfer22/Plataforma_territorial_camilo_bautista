FROM python:3.11-slim

WORKDIR /ms-analytics-scoring

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["python", "app/main.py"]
