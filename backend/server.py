import json
from flask import Flask, request
from database import DBConnection


app = Flask(__name__)

@app.route('/')
def main():
    return json.dumps({
        'api': 'waiter_bot',
        'status': 'active'
    })

db = DBConnection()

@app.route('/login', methods=['POST'])
def login():
    name, password = request.args.values()
    query = 'SELECT name, password FROM users WHERE name = ? AND password = ?'
    params = (name, password)
    try:
        data = db.read_query(query, data=params)[0]
    except Exception:
        return {'error': 'Exception raised', 'status': 500}

    if not data:
        return {'auth': False, 'status': 401}
    n, p = data
    if not (n == name and p == password):
        return {'auth': False, 'status': 401}
    return {'auth': True, 'status': 200}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
