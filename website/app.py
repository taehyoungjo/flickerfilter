import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.utils import secure_filename

from youtube import download

UPLOAD_FOLDER = '/mp4'
ALLOWED_EXTENSIONS = set(['mp4'])

# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Check if file is mp4
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        file = request.files['file']
        file.save(secure_filename(file.filename))
        return 'file uploaded'

@app.route("/fetch", methods=["GET", "POST"])
def fetch():
    if request.method == "POST":
        file_url = request.form.get("URL")
        download(file_url)
        # file_path = download(file_url)
        # bool = analyze(file_path)
        # if bool == True
        #   return render_template("")
        # else False
        #   return render_template(smth else)
        return render_template("detect_true.html")

    elif request.method == "GET":
        file_url = request.args.get("url")
        download(file_url)
        # file_path = download(file_url)
        # bool = jsonify(analyze(file_path))
        return jsonify(download(file_url))