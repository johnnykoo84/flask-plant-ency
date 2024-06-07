from flask import Flask, render_template
from db import data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('plants.html', plants=data)

@app.route('/<int:id>')
def get_plant(id):
    # find individual data with matched id
    print('id', id)
    max_len = len(data)
    if id> max_len:
        return 'Plant not found', 404
    else:
        plant = data[id]
        if plant:
            return render_template('plant.html', plant=plant)
        else:
            return 'Plant not found', 404



if __name__ == '__main__':
    app.run(debug=True)