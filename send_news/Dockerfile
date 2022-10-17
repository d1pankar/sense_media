FROM python:3.10.6-slim 

LABEL description="News service for getting news articles."

WORKDIR /app 
EXPOSE 8000
COPY requirements.txt /app/

RUN pip install -r requirements.txt 
COPY . /app/
COPY wait-for-it.sh /app/

RUN chmod +x wait-for-it.sh

