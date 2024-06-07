from flask import Flask, render_template, redirect, url_for, request
from db import data
from img_upload import handle_file_upload

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
        else:
            new_plant = {
                "id": len(data) + 1,
                "family_kor_nm": family_kor_nm,
                "genus_kor_nm": genus_kor_nm,
                "img_url": img_url,
                "plant_nm": plant_nm,
                "desc": desc,
            }
            data.append(new_plant)
            return redirect(url_for('get_all_plants'))
    return render_template("add_plant.html")

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
    
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_plant(id):
    plant_to_edit = data[id-1]
    print('plant_to_edit', plant_to_edit)
    if not plant_to_edit:
        return "Plant not found", 404

    if request.method == 'POST':
        if request.form.get('family_kor_nm', '') != '':
            plant_to_edit['family_kor_nm'] = request.form.get('family_kor_nm')
        if request.form.get('genus_kor_nm', '') != '':
            plant_to_edit['genus_kor_nm'] = request.form.get('genus_kor_nm')
        if request.form.get('plant_nm', '') != '':
            plant_to_edit['plant_nm'] = request.form.get('plant_nm')
        if request.form.get('desc', '') != '':
            plant_to_edit['desc'] = request.form.get('desc')
        
        file = request.files.get('img_file')
        img_url = handle_file_upload(file, app)
        print('img_url', img_url)
        if img_url is None:
            print('request.form.get', request.form.get('img_url'))
            if request.form.get('img_url', '') != '':
                img_url = request.form.get('img_url')
            else:
                img_url = plant_to_edit['img_url']
        plant_to_edit['img_url'] = img_url

        print('plant_to_edit.img_url', plant_to_edit['img_url'])
        data[id-1] = plant_to_edit
        return redirect(url_for('get_all_plants'))


    return render_template("edit_plant.html", plant=plant_to_edit)

if __name__ == '__main__':
    app.run(debug=True)