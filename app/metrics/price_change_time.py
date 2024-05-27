from datetime import datetime, timedelta

# Perform price movement calculations.


def price_change_time(table, results, symbol, amount, is_crypto):

    portfolio_value = 0.00
    local_currency = 'USD'
    local_symbol = '$'

    if is_crypto:
        currency = results['data'][symbol]
        name = currency['name']
        quote = currency['quote'][local_currency]
        price = quote['price']

        hour_change = round(quote['percent_change_1h'], 1)
        day_change = round(quote['percent_change_24h'], 1)
        week_change = round(quote['percent_change_7d'], 1)

        value = float(price) * float(amount)

        portfolio_value += value
    else:
        name = symbol
        last_refreshed_date = results['Meta Data']['3. Last Refreshed']
        last_refreshed_date = datetime.strptime(last_refreshed_date, '%Y-%m-%d')
        last_refreshed_date_str = last_refreshed_date.strftime('%Y-%m-%d')

        # Calculate the date of yesterday
        one_day_ago = last_refreshed_date - timedelta(days=1)
        one_day_ago_str = one_day_ago.strftime('%Y-%m-%d')

        # Calculate the date 7 days ago
        seven_days_ago = last_refreshed_date - timedelta(days=7)
        seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')

        # Hour change
        open_price = float(results['Time Series (Daily)'][last_refreshed_date_str]['1. open'])
        close_price = float(results['Time Series (Daily)'][last_refreshed_date_str]['4. close'])
        price = (open_price - close_price)/close_price * 100

        # Day change
        close_price_one_day_ago = float(results['Time Series (Daily)'][one_day_ago_str]['4. close'])
        price_day_change = (close_price - close_price_one_day_ago)/close_price_one_day_ago * 100

        # Week change
        close_price_seven_days_ago = float(results['Time Series (Daily)'][seven_days_ago_str]['4. close'])
        price_week_change = (close_price - close_price_seven_days_ago)/close_price_seven_days_ago * 100

        # Current trade volume
        amount = float(results['Time Series (Daily)'][last_refreshed_date_str]['5. volume'])

        hour_change = round(price, 1)
        day_change = round(price_day_change, 1)
        week_change = round(price_week_change, 1)

        value = float(price) * float(amount)

        portfolio_value += value

    hour_change = str(hour_change) + '%'
    day_change = str(day_change) + '%'
    week_change = str(week_change) + '%'

    price_string = '{:,}'.format(round(price, 2))
    value_string = '{:,}'.format(round(value, 2))

    table.add_row([name + ' (' + symbol + ')', amount, local_symbol + value_string, local_symbol + price_string,
                   str(hour_change), str(day_change), str(week_change), 0])

    print(f"Added new row to table for symbol {symbol}: {table}")

    return table
