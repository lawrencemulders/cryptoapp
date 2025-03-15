# cryptoapp

This readme is an introduction to a project currently being build: a notification application which generates a scheduled email providing a summary of stock/crypto performances. A simple local database is implemented, accompanied with a UI powered by Flask, to allow the user to insert/update/delete entries in the portfolio.

API's are leveraged to gather the required data from both crypto and stock assets. The user can select the relevant metrics and configure relevant metrics and daily/weekly scheduling. Leveraging an async manager to allow for multi-threading enables performant data composition, regardless of the size of one's portfolio.

![notificationflow drawio](https://github.com/lawrencemulders/cryptoapp/assets/80403668/bc434dbf-02ce-404e-8bf4-6d85fe5c0578)

Several existing features include:
- An Async Manager allowing for asynchronous I/O and multi-threading to improve performance for I/O bound operations when making HTTP requests.
- An NLP model to determine a sentiment score per asset (leveraging Reddit and Twitter API's)
- Performing API calls for other specific use cases (see main.py options 2-6)
- Allowing for scheduled notifications
- Docker container for scalability
- A frontend powered by Flask to allow the user to adjust the state of the portfolio

# frontend

Run the following command in a local terminal to initialize the application.

```ruby
% flask --app frontend run --debug
```

A database will be created allowing the user to create an account (stored on the local machine) and enter the portfolio entries. The frontend is API-enabled and runs on localhost.

# docker

To containerize this application, several steps are to be performed. The following prerequesites are assumed:
- Docker desktop is installed
- Able to run commands with this project as active directory in a suitable IDE

The application contains the necessary Dockerfile to build and run the image. Run build.sh to create an image and running container.

# env file

To enable the program on your local machine, create a local .env file within the app directory containing input for the following:

General Config
- DB_URL=sqlite:///crypto.db
- RECIPIENTEMAIL=
- SMTPUSERNAME=
- SMTPPASSWORD=
- APIKEYCRYPTO=
- APIKEYSTOCK=
- REDDITCLIENTID=
- REDDITCLIENTSECRET=
- REDDITUSERAGENT=
- TWITTERBEARERTOKEN
- CSRFSECRETKEY=

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

This mandatory step is recognized as a blocker for users. In the future, a similar construct such as AWS's API GateWay is desired to prevent each user of creating accounts.
