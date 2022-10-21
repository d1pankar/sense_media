from dotenv import load_dotenv
from producer import Producer
from omegaconf import OmegaConf
import tweepy
import os

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

producer = Producer("topic-2", "localhost:9092")

config = OmegaConf.load("<path>\config.yml")
topic = config["TwitterAPI"]["topic"]


class TweetStream(tweepy.StreamingClient):
    newTweet = {}

    def on_connect(self):
        print("Connected to Twitter API")
        print("-" * 30)

    def on_tweet(self, tweet):
        try:
            self.newTweet["tweet"] = tweet.text
            self.newTweet["date_time"] = tweet["data"]["created_at"]
        except Exception as e:
            print(e)

    def on_includes(self, includes):
        try:
            self.newTweet["username"] = includes["users"][0].username
            producer.send(self.newTweet)
        except Exception as e:
            print(e)


def main():
    query = f"{topic} lang:en -is:retweet"
    stream = TweetStream(bearer_token)
    prev_id = stream.get_rules().data[0].id
    print(stream.get_rules())
    stream.delete_rules(prev_id)
    stream.add_rules(tweepy.StreamRule(query))
    print(stream.get_rules())
    stream.filter(
        tweet_fields=["created_at", "author_id", "lang", "geo"],
        expansions=["author_id", "referenced_tweets.id", "geo.place_id"],
        user_fields=["username", "name"],
        place_fields=[
            "id",
            "country",
            "geo",
            "country_code",
            "name",
            "place_type",
            "full_name",
        ],
    )


if __name__ == "__main__":
    main()
