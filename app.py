from flask import Flask, render_template, redirect, url_for
from db import data

app = Flask(__name__)


@app.route('/')
def get_all_plants():
    return render_template('plants.html', plants=data)

@app.route('/<int:id>')
def get_plant(id):
    # find individual data with matched id
    print('id', id)
    max_len = len(data)
    if id > max_len:
        return 'Plant not found', 404
    else:
        plant = data[id-1]
        if plant:
            return render_template('plant.html', plant=plant)
        else:
            return 'Plant not found', 404

@app.route("/delete/<int:id>", methods=['POST'])
def delete_plant(id):
    print('delete_plant', id)
    max_len = len(data)
    print('max_len', max_len)

    if id > max_len:
        return 'Plant not found', 404
    else:
        del data[id-1]
        return redirect(url_for('get_all_plants'))


if __name__ == '__main__':
    app.run(debug=True)