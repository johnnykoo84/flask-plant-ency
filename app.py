from flask import Flask
from db import data

app = Flask(__name__)

@app.route('/')
def index():
    return data
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)