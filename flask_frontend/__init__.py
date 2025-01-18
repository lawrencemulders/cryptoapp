import os
from flask import Flask, g
from dotenv import load_dotenv
from .csv import CSVHandler
import logging


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        CSV_FILE_PATH=os.getenv('CSV_FILE_PATH', 'data.csv'),
    )

    if test_config:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def get_csv_handler():
        if 'csv_handler' not in g:
            g.csv_handler = CSVHandler(app.config['CSV_FILE_PATH'])
        return g.csv_handler

    @app.teardown_appcontext
    def teardown_csv_handler(exception):
        g.pop('csv_handler', None)

    # Logging setup
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Application initialized")

    from . import csv
    from . import portfolio

    app.register_blueprint(portfolio.bp)

    app.add_url_rule('/', endpoint='index')

    # CSV error handling
    csv_path = app.config['CSV_FILE_PATH']
    if not os.path.exists(csv_path):
        logger.warning(f"CSV file {csv_path} does not exist. Creating an empty one.")
        with open(csv_path, mode='w', newline='') as file:
            file.write("ticker,quantity,isCrypto\n")

    return app
