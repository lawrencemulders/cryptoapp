from pandas import DataFrame
from GoogleNews import GoogleNews
from datetime import date, timedelta
from newspaper import Article, Config
import nltk.sentiment
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.downloader.download('vader_lexicon')
nltk.download('punkt')

# Determine market sentiment using Google API webscraper.


def determine_sentiment(symbol):

    # Step 1: Extract data based on symbol

    num_pages = 1
    now = date.today()
    yesterday = date.today() - timedelta(days=1)
    google_news = GoogleNews(start=yesterday, end=now)
    google_news.search(symbol)

    for symbol in range(num_pages):
        google_news.get_page()

    result = google_news.result()
    df = DataFrame(result)

    # Step 2: Summarize found articles

    article_list = []

    for i in df.index:
        article_dict = {}
        article_obj = Article(df['link'][i], config=Config())

        try:
            article_obj.download()
            article_obj.parse()
            article_obj.nlp()
        except Exception as e:
            print(f"Error processing article {i}: {e}")
            continue  # Skip to the next iteration if an exception occurs

        article_dict['Date'] = df['date'][i]
        article_dict['Media'] = df['media'][i]
        article_dict['Title'] = article_obj.title
        article_dict['Article'] = article_obj.text
        article_dict['Summary'] = article_obj.summary
        article_dict['Key_words'] = article_obj.keywords
        article_list.append(article_dict)

    news_df = DataFrame(article_list)

    # Step 3: Sentiment analysis

    positive = 0
    negative = 0
    neutral = 0
    news_list = []
    neutral_list = []
    negative_list = []
    positive_list = []

    try:

        for news in news_df['Summary']:
            news_list.append(news)
            analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
            pos = analyzer['pos']
            neg = analyzer['neg']

            if neg > pos:
                negative_list.append(news)
                negative += 1
            elif pos > neg:
                positive_list.append(news)
                positive += 1
            elif pos == neg:
                neutral_list.append(news)
                neutral += 1

        positive_percentage = (positive / len(news_df)) * 100

        print("Sentiment:", '%.2f' % positive_percentage, end='\n')

    except KeyError:
        print(f"Failed to access Summary column in news_df: {KeyError}")
        positive_percentage = 50.0  # set to neutral

    return positive_percentage
