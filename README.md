# cryptoapp

This readme is an introduction to a project currently being build: a notification application which generates a scheduled email providing a summary of stock/crypto performances. To keep costs at zero, no database is implemented and a local csv file is used to iterate and monitor progress.

Thus far an API has been build for crypto which feeds the scheduled email providing the recipient with all reqquested metrics.

Several features include:
(1) Threading to improve performance for I/O bound operations when making HTTP requests
(2) Apply NLP models to determine a sentiment score per crypto
(3) Performing API calls for specific use cases (see main.py)

Upcoming iterations:
(1) Introduce a stock API
(2) Create configuration for the user to select interested metrics
(3) Review Hugging Face for further metrics
(4) Enable local tasks

To enable the program on your local machine, create a local .env file containing input for the following:

# General Config
- CSVFILE=
- RECIPIENTEMAIL=
- SMTPUSERNAME=
- SMTPPASSWORD=
- APIKEY=

# Metric Config
- PERCENTAGECHANGETIME=true
- SENTIMENTANALYSIS=true

# Notification Schedule Config
- SCHEDULE_DAY=sunday
- SCHEDULE_TIME=12:00

Note: APIKEY can be obtained when creating a free dev account at https://pro-api.coinmarketcap.com

Note: CSVFILE must contain a file of csv format e.g. Crypto.csv where no headers are present and column 1 contains the ticker and column 2 the amount of stock. The csv file must be stored within the project.
