from flask import Flask, render_template
from db import data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('plants.html', plants=data)
    return data
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)