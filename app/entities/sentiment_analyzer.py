from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, texts):
        """Analyze sentiment from a list of texts."""
        positive, neutral, negative = 0, 0, 0
        positive_list, neutral_list, negative_list = [], [], []

        for text in texts:
            sentiment = self.analyzer.polarity_scores(text)
            if sentiment['neg'] > sentiment['pos']:
                negative += 1
                negative_list.append(text)
            elif sentiment['pos'] > sentiment['neg']:
                positive += 1
                positive_list.append(text)
            else:
                neutral += 1
                neutral_list.append(text)

        return positive, neutral, negative
