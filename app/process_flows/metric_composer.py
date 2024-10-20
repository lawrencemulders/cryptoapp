from app.metrics.price_change_time import *
from app.metrics.sentiment_analysis import *
import os


def metric_composer(table, results, symbol, amount, is_crypto):
    # Load environment variables from .env file
    use_percentage_change_time = os.getenv("PERCENTAGECHANGETIME")
    use_sentiment_analysis = os.getenv("SENTIMENTANALYSIS")

    if use_percentage_change_time:
        metrics = PercentageChangeMetrics(table, results, symbol, amount, is_crypto)
        table = metrics.price_change_time()

    if use_sentiment_analysis:
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
                    table.rows[row_index][sentiment_column_index] = sentiment_result
                    print(f"Added sentiment score for symbol {symbol}: {sentiment_result}")
                    break  # Stop iteration after first match

    print(f"Composed all metrics for {symbol}")

    return table
