from flask import Flask, render_template, request, session, flash, url_for, send_from_directory, make_response
import os, json, re, math, subprocess
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def main():
    filelist = os.listdir('uploads')
    filedict = {}
    for _file in filelist:
        filename = ".".join(_file.split(".")[:-1])
        filetype = _file.split(".")[-1]
        if len(filename) > 0:
            filedict[_file] = {"name": filename, "type": filetype}
    return render_template('home.html', session=session, filedict=filedict)

@app.route("/about")
def about():
    return render_template('about.html', session=session)

@app.route("/explorer")
def explorer():
    return render_template('index.html', session=session)

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

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    host = str(subprocess.check_output(['ipconfig', 'getifaddr', 'en0']))[2:-3]
    print(host)
    #host = "169.231.15.119"
    app.run(debug=False, use_reloader=False, host=host, port=34197) # change use_reloader to True when running

    
