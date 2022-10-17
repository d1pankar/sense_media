from apscheduler.schedulers.background import BackgroundScheduler
from consumer import Consumer
from fastapi import FastAPI
from model import Model

from elk import ELK
import re

HOST = "http://localhost:9200"
indexName = "tweet_index"

app = FastAPI()
es = ELK(HOST)
model = Model()


def preprocess_tweets(tweet):
    tweet = re.sub("(@[A-Za-z]+[A-Za-z0-9-_]+)", "", tweet)
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub(r"bit.ly/\S+", "", tweet)
    html = re.compile("<.*?>")
    tweet = html.sub(r"", tweet)
    tweet = re.sub("([_]+)", "", tweet)
    email = re.compile(r"[\w\.-]+@[\w\.-]+")
    tweet = email.sub(r"", tweet)
    tweet = "".join(i for i in tweet if ord(i) < 128)
    tweet = tweet.lower()
    return tweet


def tweets_to_ES():
    try:
        tweet_consumer = Consumer("topic-2", "localhost:9092")
        tweets = tweet_consumer.consume()

        while True:
            for tweet in tweets:
                processed_tweet = preprocess_tweets(tweet["tweet"])

                # sentiment analysis
                sentiment = model.sentiment_analysis(processed_tweet)
                if sentiment["score"] < -3:
                    tweet["sentiment"] = "Negative"
                elif -3 <= sentiment["score"] <= 3:
                    tweet["sentiment"] = "Neutral"
                else:
                    tweet["sentiment"] = "Positive"

                # hate speech detection
                hate_speech = model.hate_speech(processed_tweet)

                if hate_speech:
                    tweet["hate_speech_type"] = hate_speech["speech_type"]
                    tweet["category_hierarchy"] = hate_speech["category_hierarchy"]

                res = es.put(tweet, indexName)
                print("tweet inserted")
                print("-" * 30)

    except Exception as e:
        print(e)


@app.get("/")
def home():
    return {"Message": "Working"}


while True:
    tweets_to_ES()
