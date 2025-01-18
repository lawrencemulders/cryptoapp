from flask import (
    Blueprint, redirect, render_template, request, url_for, current_app
)

bp = Blueprint('portfolio', __name__)


@bp.route('/portfolio')
def portfolio():
    portfolio_data = get_portfolio()
    return render_template('portfolio.html', portfolio=portfolio_data)


@bp.route('/portfolio/add', methods=['POST'])
def add_portfolio():
    ticker = request.form['ticker']
    quantity = request.form['quantity']
    is_crypto = request.form['isCrypto']
    add_to_portfolio(ticker, quantity, is_crypto)
    return redirect(url_for('views.portfolio'))


@bp.route('/portfolio/update', methods=['POST'])
def update_portfolio():
    ticker = request.form['ticker']
    quantity = request.form['quantity']
    is_crypto = request.form['isCrypto']
    update_portfolio_entry(ticker, quantity, is_crypto)
    return redirect(url_for('views.portfolio'))


@bp.route('/portfolio/delete', methods=['POST'])
def delete_portfolio():
    ticker = request.form['ticker']
    delete_from_portfolio(ticker)
    return redirect(url_for('views.portfolio'))


def get_portfolio():
    """Retrieve the entire portfolio as a list of dictionaries."""
    csv_handler = current_app.get_csv_handler()
    return csv_handler.read_all()


def get_filtered_entries(is_crypto):
    """Filter portfolio entries based on type (crypto or stock)."""
    portfolio = get_portfolio()
    return [row for row in portfolio if row['isCrypto'] == str(int(is_crypto))]


def add_to_portfolio(ticker, quantity, is_crypto):
    """Add a new entry to the portfolio."""
    csv_handler = current_app.get_csv_handler()
    csv_handler.add_entry(ticker, quantity, str(int(is_crypto)))


def update_portfolio_entry(ticker, quantity, is_crypto):
    """Update an existing portfolio entry."""
    csv_handler = current_app.get_csv_handler()
    csv_handler.update_entry(ticker, quantity, str(int(is_crypto)))


def delete_from_portfolio(ticker):
    """Delete an entry from the portfolio."""
    csv_handler = current_app.get_csv_handler()
    csv_handler.delete_entry(ticker)
