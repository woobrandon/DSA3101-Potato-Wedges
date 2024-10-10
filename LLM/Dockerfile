FROM python:3.10-slim

RUN apt update -y
RUN apt install -y curl
RUN curl https://get.docker.com/builds/Linux/x86_64/docker-latest.tgz | tar xvz -C /tmp/ && mv /tmp/docker/docker /usr/bin/docker

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY data/ ./data/
COPY templates/ ./templates/

CMD ["python", "app.py"]
