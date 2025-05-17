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

    name, password = request.args.values()
    query = 'SELECT name, password FROM users WHERE name = ?'
    params = (name,)
    try:
        data = db.read_query(query, data=params)[0]
    except mariadb.Error:
        return jsonify({
            'success' :  False,
            'message' : 'Database error'
        }), 500

    if not data[0]: # Check if database returned nothing
        return jsonify({
            'success': False,
            'message': 'No such user exists'
        }), 401

    n, p = data
    if not (n == name and p == password):
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401

    return jsonify({
        'success': True,
        'message': 'Logged in'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
