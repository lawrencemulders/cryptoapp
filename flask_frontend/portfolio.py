from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_frontend.csv import read_csv, write_csv

bp = Blueprint('portfolio', __name__)


@bp.route('/')
def index():
    posts = read_csv()
    return render_template('portfolio/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        ticker = request.form['ticker']
        quantity = request.form['quantity']
        crypto = request.form['isCrypto']

        if not ticker:
            return "Ticker is required!", 400

        posts = read_csv()
        new_post = {
            'ticker': ticker,
            'quantity': quantity,
            'isCrypto': crypto
        }
        posts.append(new_post)
        write_csv(posts)
        return redirect(url_for('portfolio.index'))

    return render_template('portfolio/create.html')


def get_asset(ticker):
    assets = read_csv()
    asset = next((a for a in assets if int(a['ticker']) == ticker), None)

    if asset is None:
        abort(404, f"Post ticker {ticker} doesn't exist.")

    return asset


@bp.route('/<string:ticker>/update', methods=('GET', 'POST'))
def update(ticker):
    asset = get_asset(ticker)

    if request.method == 'POST':
        ticker = request.form['ticker']
        quantity = request.form['quantity']
        crypto = request.form['isCrypto']
        error = None

        if not ticker:
            error = 'Ticker is required.'

        if error is not None:
            flash(error)
        else:
            assets = read_csv()
            for a in assets:
                if int(a['id']) == id:
                    a['title'] = ticker
                    a['body'] = quantity
                    a['crypto'] = crypto
                    break
            write_csv(assets)

            return redirect(url_for('portfolio.index'))

    return render_template('portfolio/update.html', post=asset)


@bp.route('/<string:ticker>/delete', methods=('POST',))
def delete(ticker):
    get_asset(ticker)

    assets = read_csv()
    updated_posts = [a for a in assets if int(a['ticker']) != ticker]

    write_csv(updated_posts)

    return redirect(url_for('portfolio.index'))
