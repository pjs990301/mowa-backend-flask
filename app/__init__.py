from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
