# cryptoapp

This readme is an introduction to a project currently being build: a notification application which generates a scheduled email providing a summary of stock/crypto performances. A simple local database is implemented, accomponied with a UI, to allow the user to insert/delete and update the portfolio.

API's are leveraged to gather the required data from both crypto and stock assets. The user can select the relevant metrics and additional daily/weekly scheduling. The full workflow of constructing each email is shown below. Leveraging threading allows for enhanced efficiency when composing performance stats.

![notificationflow drawio](https://github.com/lawrencemulders/cryptoapp/assets/80403668/bc434dbf-02ce-404e-8bf4-6d85fe5c0578)

Several existing features include:
- An Async Manager allowing for asynchronous I/O and multithreading to improve performance for I/O bound operations when making HTTP requests.
- An NLP model to determine a sentiment score per asset (leveraging Reddit and Twitter API)
- Performing API calls for other specific use cases (see main.py options 2-6)
- Allowing for scheduled emailing based on OS
- Docker container for scalability

# docker

To containerize this application, several steps are to be performed. The following prerequesites are assumed:
- Docker desktop is installed
- Able to run commands with this project as active directory in a suitable IDE

The application contains the necessary Dockerfile to build and run the image.

# env file

To enable the program on your local machine, create a local .env file within the app directory containing input for the following:

General Config
- RECIPIENTEMAIL=
- SMTPUSERNAME=
- SMTPPASSWORD=
- APIKEYCRYPTO=
- APIKEYSTOCK=
- REDDITCLIENTID=
- REDDITCLIENTSECRET=
- REDDITUSERAGENT=
- TWITTERBEARERTOKEN

Metric Config
- PERCENTAGECHANGETIME=true
- SENTIMENTANALYSIS=true

Notification Schedule Config
- SCHEDULE_DAY=sunday
- SCHEDULE_TIME=12:00

Note: APIKEYCRYPTO / APIKEYSTOCK can be obtained when creating a free dev account at https://pro-api.coinmarketcap.com / https://www.alphavantage.co/
Similiar can be done for REDDITCLIENTID, REDDITCLIENTSECRET, REDDITUSERAGENT and TWITTERBEARERTOKEN on their respective free tier developer accounts https://www.reddit.com/prefs/apps/ / https://developer.x.com/en/portal/dashboard
- Coin market cap has a free tier which limits to 10,000 daily API calls
- Alpha Vantage has a free tier which limits to 25 daily API calls
- Reddit has a free tier for 60 calls per minute
- X.com supports a free tier for 500,000 calls per month
