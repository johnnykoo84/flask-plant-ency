from flask import url_for
import os
import time

def handle_file_upload(file, app):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        original_filename = file.filename  # or use secure_filename(file.filename) for security
        timestamp = int(time.time())
        filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}{os.path.splitext(original_filename)[1]}"
        file_path = os.path.join(app.root_path, 'static/images', filename)
        print('file_path', file_path)
        file.save(file_path)
        return url_for('static', filename='images/' + filename)
    else:
        return None