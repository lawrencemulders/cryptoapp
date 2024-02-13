

def percentage_change_time(table, results, symbol, amount):

    portfolio_value = 0.00
    local_currency = 'USD'
    local_symbol = '$'

    currency = results['data'][symbol]

    name = currency['name']

    quote = currency['quote'][local_currency]

    hour_change = round(quote['percent_change_1h'], 1)
    day_change = round(quote['percent_change_24h'], 1)
    week_change = round(quote['percent_change_7d'], 1)

    price = quote['price']

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

    table.add_row([name + ' (' + symbol + ')',
                    amount,
                    local_symbol + value_string,
                    local_symbol + price_string,
                    str(hour_change),
                    str(day_change),
                    str(week_change),
                    0])
    print(f"Added new row to table: {table}")

    return table
