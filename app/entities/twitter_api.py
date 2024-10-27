from datetime import date, timedelta
import requests


class TwitterAPI:
    def __init__(self, symbol, bearer_token):
        self.symbol = symbol
        self.since_date = (date.today() - timedelta(days=1)).isoformat()  # Format as 'YYYY-MM-DD'
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"

    def create_headers(self):
        return {"Authorization": f"Bearer {self.bearer_token}"}

    def fetch_tweets(self, limit=20):
        """Fetch recent tweets related to the symbol."""
        query_params = {
            "query": f"{self.symbol} lang:en",
            "start_time": f"{self.since_date}T00:00:00Z",  # Specify start time in ISO format
            "max_results": min(limit, 100),  # X API allows up to 100 results per request
            "tweet.fields": "text",  # Return only the tweet text
        }
        headers = self.create_headers()

        response = requests.get(self.base_url, headers=headers, params=query_params)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}, {response.text}")

        data = response.json()
        tweets = [tweet["text"] for tweet in data.get("data", [])]  # Extract tweet texts

        return tweets
