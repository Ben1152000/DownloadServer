from flask import Flask, flash, render_template, request, redirect, session, flash, url_for, send_from_directory, make_response
import os, json, re, math, subprocess
from functools import wraps, update_wrapper
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getfiles(dirpath):
    filelist = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    filelist.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return filelist

@app.route("/")
def index():
    filelist = getfiles(UPLOAD_FOLDER)
    filedict = {}
    for _file in filelist:
        filename = ".".join(_file.split(".")[:-1])
        filetype = _file.split(".")[-1]
        if len(filename) > 0:
            filedict[_file] = {"name": filename, "type": filetype}
    if "error" in session:
        error = session["error"]
        del session["error"]
        return render_template('home.html', session=session, filedict=filedict, error=error)
    return render_template('home.html', session=session, filedict=filedict)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
@nocache
def download(filename):
    return send_from_directory(directory='uploads', filename=filename, as_attachment=True)

@app.route("/upload", methods=['POST'])
def upload():
    if request.form['password'] != "cato":
        session['error'] = "Incorrect password."
        return redirect(url_for('index'))
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            print("FILE: " + filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['error'] = None
            return redirect(url_for('index'))
    session['error'] = "Upload failed."
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    host = subprocess.check_output(['/bin/hostname', '-I']).strip().decode('utf-8')
    app.run(debug=False, use_reloader=False, host=host, port=8000) # change use_reloader to True when running

    
