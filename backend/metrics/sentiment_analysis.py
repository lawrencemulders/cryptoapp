import os
from backend.entities.sentiment_manager import SentimentManager


def determine_sentiment(symbol):
    reddit_client_id = os.getenv("REDDITCLIENTID")
    reddit_client_secret = os.getenv("REDDITCLIENTSECRET")
    reddit_user_agent = os.getenv("REDDITUSERAGENT")
    twitter_bearer_token = os.getenv("TWITTERBEARERTOKEN")

    sentiment_manager = SentimentManager(
        reddit_client_id=reddit_client_id,
        reddit_client_secret=reddit_client_secret,
        reddit_user_agent=reddit_user_agent,
        symbol=symbol,
        twitter_bearer_token=twitter_bearer_token,
    )

    return sentiment_manager.determine_sentiment()
