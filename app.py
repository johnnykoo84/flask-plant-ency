from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from img_upload import handle_file_upload
from flask import send_from_directory

try:
    # create the extension
    db = SQLAlchemy()
    # create the app
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.root_path, 'data.db')
    # initialize the app with the extension
    db.init_app(app)
    print('db initialized')
except Exception as e:
    print('error', e)

class DataItem(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    family_kor_nm = db.Column(db.String)  # Korean name of the family
    family_nm = db.Column(db.String)      # Scientific name of the family
    genus_kor_nm = db.Column(db.String)   # Korean name of the genus
    genus_nm = db.Column(db.String)       # Scientific name of the genus
    img_url = db.Column(db.String)        # URL of the image
    plant_nm = db.Column(db.String)  # Not recommended general name
    desc = db.Column(db.Text)  # Not recommended general name

@app.route("/")
def get_all_plants():
    data = DataItem.query.all()
    return render_template('plants.html', plants=data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/<int:id>')
def get_plant(id):
    # find individual data with matched id
    try:
        plant = DataItem.query.get(id)
        if plant:
            return render_template("plant.html", plant=plant)
        else:
            return "Plant not found", 404
    except Exception as e:
        return str(e), 500

@app.route("/add", methods=['GET','POST'])
def add_plant():
    if request.method == 'POST':
        family_kor_nm = request.form.get('family_kor_nm')
        genus_kor_nm = request.form.get('genus_kor_nm')
        plant_nm = request.form.get('plant_nm')
        desc = request.form.get('desc')
        file = request.files['img_file']

        img_url = handle_file_upload(file, app)
        if img_url is None:
            if request.form.get('img_url', '') != '':
                img_url = request.form.get('img_url')
            else:
                return "Invalid file or no file uploaded", 400
        print('family_kor_nm', family_kor_nm)
        print('genus_kor_nm', genus_kor_nm)
        print('plant_nm', plant_nm)
        print('img_url', img_url)
        print('desc', desc)
        if not plant_nm:
            return "Plant name is required", 400
        try:
            new_plant = DataItem(
                family_kor_nm=family_kor_nm,
                genus_kor_nm=genus_kor_nm,
                img_url=img_url,
                plant_nm=plant_nm,
                desc=desc,
            )
            db.session.add(new_plant)
            db.session.commit()
            return redirect(url_for('get_all_plants'))
        except Exception as e:
            db.session.rollback()
            return str(e), 500
    return render_template("add.html")

@app.route("/delete/<int:id>", methods=['POST'])
def delete_plant(id):
    print('delete_plant', id)
    try:
        plant_to_delete = DataItem.query.get(id)
        if plant_to_delete:
            db.session.delete(plant_to_delete)
            db.session.commit()
            return redirect(url_for('get_all_plants'))
        else:
            return "Plant not found", 404
    except Exception as e:
        return str(e), 500

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_plant(id):
    plant_to_edit = DataItem.query.get(id)
    if not plant_to_edit:
        return "Plant not found", 404

    if request.method == 'POST':
        if request.form.get('family_kor_nm', '') != '':
            plant_to_edit.family_kor_nm = request.form.get('family_kor_nm')
        if request.form.get('genus_kor_nm', '') != '':
            plant_to_edit.genus_kor_nm = request.form.get('genus_kor_nm')
        if request.form.get('plant_nm', '') != '':
            plant_to_edit.plant_nm = request.form.get('plant_nm')
        if request.form.get('desc', '') != '':
            plant_to_edit.desc = request.form.get('desc')
        
        file = request.files.get('img_file')
        img_url = handle_file_upload(file, app)
        print('img_url', img_url)
        if img_url is None:
            print('image url from form', request.form.get('img_url'))
            if request.form.get('img_url', '') != '':
                img_url = request.form.get('img_url')
            else:
                img_url = plant_to_edit.img_url
        if plant_to_edit.img_url != img_url:
            plant_to_edit.img_url = img_url

        try:
            print('plant_to_edit.img_url', plant_to_edit.img_url)
            db.session.commit()
            return redirect(url_for('get_all_plants'))
        except Exception as e:
            db.session.rollback()
            print(e)
            return str(e), 500

    return render_template("edit.html", plant=plant_to_edit)



@app.route('/img/<filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == "__main__":
    app.run(debug=True, port=5001)