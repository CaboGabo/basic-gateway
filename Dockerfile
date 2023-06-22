FROM python:3.9.17-slim-buster

WORKDIR /app/src

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src .

EXPOSE 8000
