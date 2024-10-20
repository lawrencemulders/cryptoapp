import requests


class CryptoAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://pro-api.coinmarketcap.com'

    def fetch_data(self, symbol):
        # Establish API call parameters
        quote_url = self.base_url + '/v1/cryptocurrency/quotes/latest?convert=USD&symbol=' + symbol
        headers = {'X-CMC_PRO_API_KEY': self.api_key}

        # Perform Get call
        response = requests.get(quote_url, headers=headers)

        # Handle response
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        return response.json()  # Return parsed json
