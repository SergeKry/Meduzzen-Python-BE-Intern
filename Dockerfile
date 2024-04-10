# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3","app/main.py"]
