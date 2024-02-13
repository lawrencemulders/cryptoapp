from metrics.percentage_change_time import *
from metrics.sentiment_analysis import *


def metric_composer(table, results, symbol, amount):

    table = percentage_change_time(table, results, symbol, amount)

    # Find the index of the "Sentiment" column
    sentiment_column_name = "Sentiment"
    sentiment_column_index = None

    # Assuming the first row contains column headers
    headers = table.field_names

    for i, header in enumerate(headers):
        if header == sentiment_column_name:
            sentiment_column_index = i
            break

    if sentiment_column_index is None:
        print("Error: Column '{}' not found in the table.".format(sentiment_column_name))
    else:
        sentiment_result = determine_sentiment(symbol)

        # Iterate through the table to find the row with the specified symbol
        for row_index in range(len(table.rows)):
            if symbol in table.rows[row_index][0].upper():
                table._rows[row_index][sentiment_column_index] = sentiment_result
                break  # Stop iteration after the first match

    print(table)
    return table
