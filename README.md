# cryptoapp

This readme is an introduction to a project currently being build: a notification application which generates a scheduled email providing a summary of stock/crypto performances. To keep costs at zero, no database is implemented and a local csv file is used to iterate and monitor progress.

API's are leveraged to gather the required data from both crypto and stock assets. The user can select the relevant metrics and additional weekly/daily scheduling.

Several features include:
(1) Threading to improve performance for I/O bound operations when making HTTP requests
(2) Apply NLP models to determine a sentiment score per crypto
(3) Performing API calls for specific use cases (see main.py)
(4) Allowing for scheduled emailing based on a container (Docker) and launchd (macOS-specific)

Upcoming iterations:
(1) Review Hugging Face for further metrics
(2) Expand stock API use cases
(3) Introduce a website to allow for a user-friendly installation guide

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

# Docker and Launchd (macOS specific)

To containerize this application, several steps are to be performed. The following prerequesites are assumed:
- Docker desktop is installed
- Able to run commands with this project as active directory in a suitable IDE

The application contains the necessary Dockerfile to containerize and create the image. However, 2 commands must be executed to initialize the scheduling:
- docker build -t python-cryptoapp -f docker/Dockerfile .
- docker run -i -t python-cryptoapp

In addition to running the commands, to enable scheduled emails, an additional step is required to be performed: run main.py and select option 7. This will create an initial plist file which will trigger a process flow to generate an email based on the configuration provided in the .env file (SCHEDULE_DAY and SCHEDULE_TIME)
