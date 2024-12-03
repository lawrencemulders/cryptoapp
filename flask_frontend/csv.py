import csv
import os


class CSVHandler:
    def __init__(self, file_path='data.csv'):
        self.file_path = file_path

    def ensure_file_exists(self):
        """Ensure the CSV file exists and has the correct headers."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ticker', 'quantity', 'isCrypto'])

    def read_all(self):
        """Read all data from the CSV file."""
        self.ensure_file_exists()
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def add_entry(self, ticker, quantity, is_crypto):
        """Add a new entry to the CSV file."""
        self.ensure_file_exists()
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ticker, quantity, is_crypto])

    def update_entry(self, ticker, quantity, is_crypto):
        """Update an entry in the CSV file."""
        data = self.read_all()
        updated = False
        for row in data:
            if row['ticker'] == ticker:
                row['quantity'] = quantity
                row['isCrypto'] = is_crypto
                updated = True
        if updated:
            self._write_all(data)
        else:
            raise ValueError(f"Ticker {ticker} not found in the CSV file.")

    def delete_entry(self, ticker):
        """Delete an entry from the CSV file."""
        data = self.read_all()
        filtered_data = [row for row in data if row['ticker'] != ticker]
        if len(data) == len(filtered_data):
            raise ValueError(f"Ticker {ticker} not found in the CSV file.")
        self._write_all(filtered_data)

    def _write_all(self, data):
        """Write all data back to the CSV file."""
        with open(self.file_path, mode='w', newline='') as file:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(file)
                writer.writerow(['ticker', 'quantity', 'isCrypto'])
