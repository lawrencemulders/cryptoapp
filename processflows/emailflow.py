import numpy as np
import schedule
from communication.emailgenerator import *

#  1) Access local csv file
#  TODO: create configuration file where user specifies which csv file to use

with open(csvfile, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        if "\ufeff" in line[0]:
            line[0] = line[0][1:].upper()
        else:
            line[0] = line[0].upper()

        symbol = line[0]
        amount = line[1]

#  2) Perform API calls
#  TODO: define api implementation for stocks and assess retrieved data
#  TODO: establish mapping between api results and local variables

#  3) Perform necessary calculations


#  4) Persist upon csv file


#  5) Retrieve data from csv file


#  6) Generate scheduled email

schedule.every().sunday.at('12:00').do(send_scheduled_email)
while True:
    schedule.run_pending()
    time.sleep(1)