from datetime import datetime, timedelta


def percentage_change_time(table, results, symbol, amount, is_crypto):

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

        # Calculate the date 7 days ago
        seven_days_ago = last_refreshed_date - timedelta(days=7)
        seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')

        open_price = float(results['Time Series (Daily)'][last_refreshed_date_str]['1. open'])
        price = float(results['Time Series (Daily)'][last_refreshed_date_str]['4. close'])
        amount = float(results['Time Series (Daily)'][last_refreshed_date_str]['5. volume'])
        close_price_seven_days_ago = float(results['Time Series (Daily)'][seven_days_ago_str]['4. close'])

        print(open_price)
        print(price)
        print(amount)
        print(close_price_seven_days_ago)

        hour_change = round(open_price, 1)
        day_change = round(price, 1)
        week_change = round(close_price_seven_days_ago, 1)

        value = float(price) * float(amount)

        portfolio_value += value

    if hour_change > 0:
        hour_change = str(hour_change) + '%'
    else:
        hour_change = str(hour_change) + '%'

    if day_change > 0:
        day_change = str(day_change) + '%'
    else:
        day_change = str(day_change) + '%'

    if week_change > 0:
        week_change = str(week_change) + '%'
    else:
        week_change = str(week_change) + '%'

    price_string = '{:,}'.format(round(price, 2))
    value_string = '{:,}'.format(round(value, 2))

    table.add_row([name + ' (' + symbol + ')', amount, local_symbol + value_string, local_symbol + price_string,
                   str(hour_change), str(day_change), str(week_change), 0])

    print(f"Added new row to table: {table}")

    return table
