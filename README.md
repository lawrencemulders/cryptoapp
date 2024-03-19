# cryptoapp

This readme is an introduction to a project currently being build: a notification application which generates a scheduled email providing a summary of stock/crypto performances. To keep costs at zero, no database is implemented and a local csv file is used to iterate and monitor progress.

Thus far an API has been build for crypto which feeds the scheduled email providing the recipient with all reqquested metrics.

Several features include:
(1) Threading to improve performance for I/O bound operations when making HTTP requests
(2) Apply NLP models to determine a sentiment score per crypto
(3) Performing API calls for specific use cases (see main.py)

Upcoming iterations:
(1) Review Hugging Face for further metrics
(2) Enable local tasks
(3) Expand stock API use cases
(4) Allow for modifying the excel to keep track of historical progress

# Env File

To enable the program on your local machine, create a local .env file containing input for the following:

General Config
- CSVFILE=
- RECIPIENTEMAIL=
- SMTPUSERNAME=
- SMTPPASSWORD=
- APIKEYCRYPTO=
- APIKEYSTOCK=

Metric Config
- PERCENTAGECHANGETIME=true
- SENTIMENTANALYSIS=true

Notification Schedule Config
- SCHEDULE_DAY=sunday
- SCHEDULE_TIME=12:00

Note: APIKEYCRYPTO / APIKEYSTOCK can be obtained when creating a free dev account at https://pro-api.coinmarketcap.com / https://www.alphavantage.co/
- Coin market cap has a free tier which limits to 10,000 API calls
- Alpha Vantage has a free tier which limits to 25 API calls

Note: CSVFILE must contain a file of csv format e.g. Crypto.csv where no headers are present and column 1 contains the ticker column 2 the quanityt of each asset, and column 3 must contain either 0 (stock) or 1 (crypto). The csv file must be stored within the project.
