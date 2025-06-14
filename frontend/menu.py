from flask import (
    Blueprint, render_template, request, jsonify
)
from backend.main import (
    generate_email_flow, market_overview_crypto, list_crypto, single_search_crypto, top100_crypto
)
from frontend.auth import login_required
import asyncio

bp = Blueprint('menu', __name__)


@bp.route('/menu', methods=['GET'])
@login_required
def select_option():
    return render_template('menu/choice.html')


@bp.route('/menu/execute', methods=['POST'])
@login_required
def execute_option():
    data = request.json
    option = data.get('option')

    try:
        if option == '1':
            table = asyncio.run(generate_email_flow())
            result = str(table)
        elif option == '2':
            result = market_overview_crypto()
        elif option == '3':
            result = list_crypto()
        elif option == '4':
            ticker = data.get('ticker')
            result = single_search_crypto(ticker)
        elif option == '5':
            sort_by = data.get('sort_by')
            table = top100_crypto(sort_by)
            result = str(table)
        else:
            result = "Invalid option"
    except Exception as e:
        result = f"Error occurred: {str(e)}"

    return jsonify({'result': result})
