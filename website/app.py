import os

from cs50 import SQL

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.utils import secure_filename

from youtube import download
from algorithm import analyze

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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///flickerfilter.db")

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
        filename = secure_filename(file.filename)
        file.save(os.path.join('./epilepsy_videos', filename))
        file_path = "./epilepsy_videos/" + filename
        print(file_path)
        result = analyze(file_path)
        os.remove(file_path)
        if result == True:
            return render_template("detect_true.html")
        else:
            return render_template("detect_false.html")

@app.route("/fetch", methods=["GET", "POST"])
def fetch():
    if request.method == "POST":
        file_url = request.form.get("URL")
        id = file_url.split('=')
        query = db.execute("SELECT result FROM videos WHERE id=:id", id=id[1])
        if query:
            if query[0]['result'] == 0:
                result = False
            else:
                result = True
        else:
            download(file_url)
            file_path = "./epilepsy_videos/" + id[1] + ".mp4"
            result = analyze(file_path)
            os.remove(file_path)
            add = db.execute('INSERT INTO "videos" ("id","result") VALUES (:id, :result)', id=id[1], result=result)
        if result == True:
            return render_template("detect_true.html")
        else:
            return render_template("detect_false.html")

    elif request.method == "GET":
        file_url = request.args.get("url")
        id = file_url.split('=')
        query = db.execute("SELECT result FROM videos WHERE id=:id", id=id[1])
        if query:
            if query[0]["result"] == 0:
                return jsonify(False)
            else:
                return jsonify(True)
        else:
            download(file_url)
            file_path = "./epilepsy_videos/" + id[1] + ".mp4"
            print(file_path)
            result = analyze(file_path)
            os.remove(file_path)
            if result == False:
                result_bool = 0
            else:
                result_bool = 1
            add = db.execute('INSERT INTO "videos" ("id","result") VALUES (:id, :result)', id=id[1], result=result_bool)
            return jsonify(result)