# cryptoapp

This readme is an introduction to a project currently being build: a notification application which generates a scheduled email providing a summary of stock/crypto performances. To keep costs at zero, no database is implemented and a local csv file is used to iterate and monitor progress.

Thus far an API has been build for crypto which feeds the scheduled email providing the recipient with all reqquested metrics.

Upcoming iterations:
(1) Apply NLP models to determine a sentiment score per crypto
(2) Introduce a stock API
(3) Create configuration for the user to select interested metrics

To enable the program on your local machine, create a local .env file containing input for the following:

CSVFILE=
RECIPIENTEMAIL=
SMTPUSERNAME=
SMTPPASSWORD=
APIKEY=

Note: CSVFILE must contain a file of csv format e.g. Crypto.csv where no headers are present and column 1 contains the ticker and column 2 the amount of stock. The csv file must be stored within the project.
