import csv
import os
from flask import current_app


def read_csv():
    if not os.path.exists(current_app.config['CSV_FILE_PATH']):
        return []
    with open(current_app.config['CSV_FILE_PATH'], mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def write_csv(data):
    if not data:
        return  # Do nothing if there's no data
    with open(current_app.config['CSV_FILE_PATH'], mode='w', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    current_app.read_csv = read_csv
    current_app.write_csv = write_csv
