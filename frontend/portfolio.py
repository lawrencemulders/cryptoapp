from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from frontend.auth import login_required
from backend.db import get_db

bp = Blueprint('portfolio', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, ticker, quantity, is_crypto, created, author_id, username'
        ' FROM portfolio p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('portfolio/index.html', posts=posts)


def get_portfolio(id, check_author=True):
    portfolio = get_db().execute(
        'SELECT p.id, ticker, quantity, is_crypto, created, author_id, username'
        ' FROM portfolio p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if portfolio is None:
        abort(404, f"Portfolio id {id} doesn't exist.")

    if check_author and portfolio['author_id'] != g.user['id']:
        abort(403)

    return portfolio


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        ticker = request.form['ticker']
        quantity = request.form['quantity']
        is_crypto = 1 if request.form.get('is_crypto') else 0
        error = None

        if not ticker:
            error = 'Ticker is required.'
        if not quantity:
            error = 'Quantity is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO portfolio (author_id, ticker, quantity, is_crypto)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], ticker, quantity, is_crypto)
            )
            db.commit()
            return redirect(url_for('portfolio.index'))

    return render_template('portfolio/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_portfolio(id)

    if request.method == 'POST':
        ticker = request.form['ticker']
        quantity = request.form['quantity']
        is_crypto = 1 if request.form.get('is_crypto') else 0
        error = None

        if not ticker:
            error = 'Ticker is required.'
        if not quantity:
            error = 'Quantity is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE portfolio SET ticker = ?, quantity = ?, is_crypto = ?'
                ' WHERE id = ?',
                (ticker, quantity, is_crypto, id)
            )
            db.commit()
            return redirect(url_for('portfolio.index'))

    return render_template('portfolio/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST', 'DELETE'))
@login_required
def delete(id):
    get_portfolio(id)
    db = get_db()
    db.execute('DELETE FROM portfolio WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('portfolio.index'))
