from apscheduler.schedulers.background import BackgroundScheduler
from omegaconf import OmegaConf
from consumer import Consumer
from fastapi import FastAPI
from model import Model
from elk import ELK

app = FastAPI()

HOST = "http://localhost:9200"

config = OmegaConf.load("<path>\config.yml")
indexName = "news_index"

try:
    es = ELK(HOST)
    print("Connection:", es.ping())
    print("-" * 30)
    # create new index
    # res = es.create_index(indexName=indexName)
    # print(res, end="--> success\n")

except Exception as e:
    print(e)


model = Model()


def get_data():
    try:

        news_consumer = Consumer("topic-1", "localhost:9092")
        messages = news_consumer.consume()

        for msg in messages:
            desc = msg["message"]["description"]
            sentiment = model.sentiment_analysis(desc)
            print(sentiment)
            msg["message"]["sentiment_score"] = sentiment["score"]

            if sentiment["score"] < -5:
                msg["message"]["sentiment"] = "Negative"
            elif -5 <= sentiment["score"] <= 5:
                msg["message"]["sentiment"] = "Neutral"
            else:
                msg["message"]["sentiment"] = "Positive"
            res = es.put(msg["message"], indexName)
            print("-----inserted------")
    except Exception as e:
        print(e)


@app.get("/")
def home():
    return {"message": "Working fine"}


get_data()

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(get_data(), "interval", minutes=1440)  # run every day
scheduler.start()
