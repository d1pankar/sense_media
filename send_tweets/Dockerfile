FROM python:3.10.6-slim 

LABEL description="Tweets service for getting tweets."

WORKDIR /app 

COPY requirements.txt /app/

RUN pip install -r requirements.txt 

COPY . /app/
COPY wait-for-it.sh /app/

RUN chmod +x wait-for-it.sh

