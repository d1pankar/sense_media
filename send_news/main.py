from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
from producer import Producer
from omegaconf import OmegaConf
from fastapi import FastAPI
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

producer = Producer("topic-1", "localhost:9092")

app = FastAPI()

print("Connected to kafka")
enddate = date.today()
startdate = date.today() - timedelta(days=1)

config = OmegaConf.load("<path>\config.yml")
topic = config["NewsAPI"]["topic"]
api_key = os.getenv("NEWS_API_KEY")


def send_data():
    try:
        print("connecting")
        res = requests.get(
            f"https://newsapi.org/v2/everything?q={topic}&from={startdate}&to={enddate}&language=en&apiKey={api_key}"
        )
        data = res.json()
        articles = data["articles"]

        for article in articles:
            news = {}
            news["title"] = article["title"]
            news["description"] = article["description"]
            news["date_time"] = article["publishedAt"]
            news["source"] = article["source"]["name"]
            print("Sending news...")
            producer.send({"message": news})
            time.sleep(1)
    except Exception as e:
        print(e)


@app.get("/")
def home():
    return {"message": "working fine"}


send_data()

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(send_data(), "interval", minutes=1441)  # run every day
scheduler.start()
