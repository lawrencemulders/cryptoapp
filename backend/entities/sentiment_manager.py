from backend.entities.reddit_api import RedditAPI
from backend.entities.sentiment_analyzer import SentimentAnalyzer
from backend.entities.twitter_api import TwitterAPI


class SentimentManager:
    def __init__(self, reddit_client_id, reddit_client_secret, reddit_user_agent, symbol, twitter_bearer_token):
        self.symbol = symbol
        self.reddit_api = RedditAPI(reddit_client_id, reddit_client_secret, reddit_user_agent)
        self.twitter_api = TwitterAPI(symbol, twitter_bearer_token)  # Pass Bearer Token for Twitter API
        self.sentiment_analyzer = SentimentAnalyzer()

    def determine_sentiment(self):
        """Fetch posts from Reddit and X (formerly Twitter) and analyze their sentiment."""

        # Fetch data from Reddit
        reddit_posts = self.reddit_api.fetch_posts(self.symbol)

        # Fetch data from X (Twitter)
        try:
            twitter_posts = self.twitter_api.fetch_tweets()
        except Exception as e:
            print(f"Error fetching Twitter data: {e}")
            twitter_posts = []  # Set to empty list if fetching fails

        # Combine posts from both platforms
        combined_posts = reddit_posts + twitter_posts

        # Analyze sentiment
        positive, neutral, negative = self.sentiment_analyzer.analyze_sentiment(combined_posts)
        total = len(combined_posts)

        # Calculate sentiment percentages
        if total > 0:
            positive_percentage = (positive / total) * 100
            neutral_percentage = (neutral / total) * 100
            negative_percentage = (negative / total) * 100
        else:
            positive_percentage = neutral_percentage = negative_percentage = 0

        print(f"Sentiment for {self.symbol}:")
        print(f"Positive: {positive_percentage:.2f}%")
        print(f"Neutral: {neutral_percentage:.2f}%")
        print(f"Negative: {negative_percentage:.2f}%")

        # Return net sentiment score
        return positive_percentage - negative_percentage
