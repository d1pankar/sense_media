FROM python:3.10.6-slim 

LABEL description="News service for getting news articles."

WORKDIR /app 

COPY requirements.txt /app/

RUN pip install -r requirements.txt 

COPY . /app/

