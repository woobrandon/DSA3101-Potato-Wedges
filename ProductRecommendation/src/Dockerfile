FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY data/ ./data/
COPY templates/ ./templates/

RUN mkdir -p /app/models

CMD ["python", "app.py"]