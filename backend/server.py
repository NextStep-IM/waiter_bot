from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def main():
    return json.dumps({
        'api': 'waiter_bot',
        'status': 'active'
    })




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
