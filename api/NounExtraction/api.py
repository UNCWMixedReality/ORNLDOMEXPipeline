import os
from posixpath import curdir

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

api_bp = Blueprint("api_v1", __name__)

ALLOWED_EXTENSIONS = {"txt", "pdf", "doc", "docx", "zip"}

# Helper Functions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes
@api_bp.route("/zip_upload/", methods=["GET", "POST"])
def zip_upload():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("api_v1.download_file", name=filename))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


@api_bp.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)
