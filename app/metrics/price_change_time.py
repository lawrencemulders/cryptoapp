from datetime import datetime, timedelta


class PercentageChangeMetrics:

    def __init__(self, table, results, symbol, amount, is_crypto):
        self.table = table
        self.results = results
        self.symbol = symbol
        self.amount = amount
        self.is_crypto = is_crypto
        self.local_currency = 'USD'
        self.local_symbol = '$'
        self.portfolio_value = 0.00

    def calculate_percentage_change(self, new_value, old_value):
        return (new_value - old_value) / old_value * 100

    def format_value(self, value):
        return '{:,}'.format(round(value, 2))

    def get_crypto_data(self):
        currency = self.results['data'][self.symbol]
        name = currency['name']
        quote = currency['quote'][self.local_currency]
        price = quote['price']

        hour_change = round(quote['percent_change_1h'], 1)
        day_change = round(quote['percent_change_24h'], 1)
        week_change = round(quote['percent_change_7d'], 1)

        value = float(price) * float(self.amount)

        return name, price, value, hour_change, day_change, week_change

    def get_stock_data(self):
        name = self.symbol
        last_refreshed_date_str = self.results['Meta Data']['3. Last Refreshed']
        last_refreshed_date = datetime.strptime(last_refreshed_date_str, '%Y-%m-%d')

        one_day_ago_str = (last_refreshed_date - timedelta(days=1)).strftime('%Y-%m-%d')
        seven_days_ago_str = (last_refreshed_date - timedelta(days=7)).strftime('%Y-%m-%d')

        # Current prices
        open_price = float(self.results['Time Series (Daily)'][last_refreshed_date_str]['1. open'])
        close_price = float(self.results['Time Series (Daily)'][last_refreshed_date_str]['4. close'])
        close_price_one_day_ago = float(self.results['Time Series (Daily)'][one_day_ago_str]['4. close'])
        close_price_seven_days_ago = float(self.results['Time Series (Daily)'][seven_days_ago_str]['4. close'])

        # Calculate changes
        hour_change = self.calculate_percentage_change(open_price, close_price)
        day_change = self.calculate_percentage_change(close_price, close_price_one_day_ago)
        week_change = self.calculate_percentage_change(close_price, close_price_seven_days_ago)

        # Volume (amount of shares traded)
        value = float(self.results['Time Series (Daily)'][last_refreshed_date_str]['5. volume'])

        return name, close_price, value, hour_change, day_change, week_change

    def add_row_to_table(self, name, symbol, amount, value, price, hour_change, day_change, week_change):
        value_string = self.format_value(value)
        price_string = self.format_value(price)

        self.table.add_row([
            f"{name} ({symbol})",
            amount,
            f"{self.local_symbol}{value_string}",
            f"{self.local_symbol}{price_string}",
            f"{hour_change}%",
            f"{day_change}%",
            f"{week_change}%",
            0
        ])

        print(f"Added new row to table for symbol {symbol}: {self.table}")

    def price_change_time(self):
        if self.is_crypto:
            name, price, value, hour_change, day_change, week_change = self.get_crypto_data()
        else:
            name, price, value, hour_change, day_change, week_change = self.get_stock_data()

        # Update portfolio value
        self.portfolio_value += value

        # Add the row to the table
        self.add_row_to_table(name, self.symbol, self.amount, value, price, hour_change, day_change, week_change)

        return self.table
