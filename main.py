import os
from app import app
from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    """
    Choose a file from the local system to upload
    :return:
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


@app.route('/')
def download_form():
    return render_template('download.html')


@app.route('/download', methods=['GET'])
def download_file():
    """
    Give the path, from which location the file is to be downloaded
    :return:
    """
    path = "D:\sample.txt"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run()
