import json
from typing import Tuple

import mariadb
from flask import Flask, request, Response, session
from flask import jsonify
from .database import DBConnection


app = Flask(__name__)
app.secret_key = b'a524ef4d9e3a62d5bdfcfbf49a213e02070a50dd6fbcfe8134d5f9961d31620c'
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

    :return: The response in json and status code
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

    session['username'] = name
    return jsonify({
        'success': True,
        'message': 'Logged in'
    }), 200

# TODO: Finish this
@app.route('/signup', methods=['POST'])
def signup() -> Tuple[Response, int]:
    """
    Register the user

    :return: The response in json and status code
    :rtype: Tuple[Response, int]
    """
    response = request.get_json()
    name = response['name']
    password = response['password']
    try:
        if db.user_exists(name):
            return jsonify({
                'success': False,
                'message': 'User already exists'
            }), 409

        db.signup_user(name, password)
    except mariadb.Error:
        return jsonify({
            'success' :  False,
            'message' : 'Database error. Failed to register user.'
        }), 500

    return jsonify({
        'success': True,
        'message': 'User has been signed up.'
    }), 200

# NOTE: Maybe using an int id instead of username will be better
@app.route('/user', methods=['GET'])
def get_user():

    if 'username' in session:
        print(f'/get_user: Username: {session['username']} saved in session')

        # TODO: This is a workaround. Use Flask-Login
        first_time_login: bool = db.is_first_time(session['username'])
        print(f'This is get_user(). First time login is {first_time_login}')
        return {
            'success': True,
            'message': {
                'username': session['username'],
                'first_time': first_time_login
            }
        }, 200

    return {
        'success': False,
        'message': 'User not logged in.'
    }, 401


@app.route('/recommend')
def recommend():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
