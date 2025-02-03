import requests


class StockAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'

    def fetch_data(self, symbol):
        """Fetch data points related to the symbol."""
        quote_url = self.base_url + '&symbol=' + symbol + '&outputsize=compact&apikey=' + self.api_key

        # Perform Get call
        response = requests.get(quote_url)

        # Handle response
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        return response.json()  # Return parsed json
