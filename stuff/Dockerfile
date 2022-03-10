# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /

COPY requirements2.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
