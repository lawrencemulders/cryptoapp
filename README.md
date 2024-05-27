# cryptoapp

This readme is an introduction to a project currently being build: a notification application which generates a scheduled email providing a summary of stock/crypto performances. To keep costs at zero, no database is implemented and a local csv file is used to monitor progress.

API's are leveraged to gather the required data from both crypto and stock assets. The user can select the relevant metrics and additional daily/weekly scheduling. The full workflow of constructing each email is shown below. Leveraging threading allows for enhanced efficiency when composing performance stats.

![notificationflow drawio](https://github.com/lawrencemulders/cryptoapp/assets/80403668/bc434dbf-02ce-404e-8bf4-6d85fe5c0578)

Several existing features include:
(1) Threading to improve performance for I/O bound operations when making HTTP requests
(2) Apply NLP models to determine a sentiment score per asset
(3) Performing API calls for specific use cases (see main.py options 2-6)
(4) Allowing for scheduled emailing based on a container (Docker) and launchd (macOS-specific)

Upcoming iterations:
(1) Expand upon error handling when necessary installation steps are not followed e.g. insufficient .env file
(2) Introduce a site using Flask to allow for a user-friendly installation guide

# Env File

To enable the program on your local machine, create a local .env file within the app directory containing input for the following:

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
- Coin market cap has a free tier which limits to 10,000 daily API calls
- Alpha Vantage has a free tier which limits to 25 daily API calls

Note: CSVFILE must contain a file of csv format e.g. Crypto.csv where no headers are present and column 1 contains the ticker column 2 the quanityt of each asset, and column 3 must contain either 0 (stock) or 1 (crypto). The csv file must be stored within the app directory.

# Docker and Launchd (macOS specific)

To containerize this application, several steps are to be performed. The following prerequesites are assumed:
- Docker desktop is installed
- Able to run commands with this project as active directory in a suitable IDE

The application contains the necessary Dockerfile to build and run the image based on .env configuration. However, the build.sh file must be run locally to enable scheduled notifications based on the configuration provided in the .env file (SCHEDULE_DAY and SCHEDULE_TIME). 

When the user re-runs Build.sh, a new plist file will be generated using the current configuration in the .env file.
