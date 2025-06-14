from flask import Flask
import logging
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))


def create_app(test_config=None):

    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_URL=os.getenv("DB_URL"),
    )

    if test_config:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
        print(f"Instance path: {app.instance_path}")
    except OSError:
        pass

    # Logging setup
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Application initialized")

    from backend import db
    from . import portfolio
    from . import auth
    from . import menu

    db.init_app(app)
    app.register_blueprint(portfolio.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(menu.bp)

    return app
