from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from frontend.auth import login_required
from backend.db import get_db
import psycopg2.extras

bp = Blueprint('portfolio', __name__)


@bp.route('/portfolio')
def index():
    conn = get_db()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('''
            SELECT p.id, ticker, quantity, is_crypto, created, author_id, username
            FROM portfolio p
            JOIN "user" u ON p.author_id = u.id
            ORDER BY created DESC
        ''')
        posts = cur.fetchall()
    return render_template('portfolio/index.html', posts=posts)


def get_portfolio(id, check_author=True):
    conn = get_db()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('''
            SELECT p.id, ticker, quantity, is_crypto, created, author_id, username
            FROM portfolio p
            JOIN "user" u ON p.author_id = u.id
            WHERE p.id = %s
        ''', (id,))
        portfolio = cur.fetchone()

    if portfolio is None:
        abort(404, f"Portfolio id {id} doesn't exist.")

    if check_author and portfolio['author_id'] != g.user['id']:
        abort(403)

    return portfolio


@bp.route('/portfolio/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip()
        quantity_raw = request.form.get('quantity', '').strip()
        is_crypto = bool(request.form.get('is_crypto'))
        error = None

        if not ticker:
            error = 'Ticker is required.'

        try:
            quantity = float(quantity_raw)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            error = 'Quantity must be a positive number.'

        if error:
            flash(error)
        else:
            conn = get_db()
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO portfolio (author_id, ticker, quantity, is_crypto)
                    VALUES (%s, %s, %s, %s)
                ''', (g.user['id'], ticker, quantity, is_crypto))
                conn.commit()
            return redirect(url_for('portfolio.index'))

    return render_template('portfolio/create.html')


@bp.route('/portfolio/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_portfolio(id)

    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip()
        quantity_raw = request.form.get('quantity', '').strip()
        is_crypto = bool(request.form.get('is_crypto'))
        error = None

        if not ticker:
            error = 'Ticker is required.'

        try:
            quantity = float(quantity_raw)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            error = 'Quantity must be a positive number.'

        if error:
            flash(error)
        else:
            conn = get_db()
            with conn.cursor() as cur:
                cur.execute('''
                    UPDATE portfolio
                    SET ticker = %s, quantity = %s, is_crypto = %s
                    WHERE id = %s
                ''', (ticker, quantity, is_crypto, id))
                conn.commit()
            return redirect(url_for('portfolio.index'))

    return render_template('portfolio/update.html', post=post)


@bp.route('/portfolio/<int:id>/delete', methods=('POST', 'DELETE'))
@login_required
def delete(id):
    get_portfolio(id)
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('DELETE FROM portfolio WHERE id = %s', (id,))
        conn.commit()
    return redirect(url_for('portfolio.index'))
