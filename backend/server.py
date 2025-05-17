import json
from typing import Tuple

import mariadb
from flask import Flask, request, Response
from flask import jsonify
from .database import DBConnection


app = Flask(__name__)

@app.route('/')
def main():
    return jsonify({
        'api': 'waiter_bot',
        'status': 'active'
    })

db = DBConnection()

@app.route('/login', methods=['POST'])
def login() -> Tuple[Response, int]:
    """
    Login to the website

    :return: A tuple containing the response json and status code
    :rtype: Tuple[Response, int]
    """

    response = request.get_json()
    name = response['name']
    password = response['password']

    try:
        if not db.authenticate_user(name, password):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
    except mariadb.Error:
        return jsonify({
            'success' :  False,
            'message' : 'Database error'
        }), 500

    return jsonify({
        'success': True,
        'message': 'Logged in'
    }), 200

# TODO: Finish this
@app.route('/signup', methods=['POST'])
def signup():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
