import json
import os
from posixpath import curdir

from celery.result import AsyncResult
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from NounExtraction.async_extraction import (
    classify_new_file,
    classify_new_zip,
    create_task,
)
from NounExtraction.auth import KeyManager
from werkzeug.utils import secure_filename

api_bp = Blueprint("api_v1", __name__)

ALLOWED_EXTENSIONS = {"zip", "pdf", "txt", "doc", "docx"}

KM = KeyManager()

# Helper Functions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def results_upload(results, task_id):
    os.makedirs(current_app.config["RESULTS_FOLDER"], exist_ok=True)
    new_filename = os.path.join(current_app.config["RESULTS_FOLDER"], f"{task_id}.json")
    with open(new_filename, "w") as ifile:
        ifile.write(results)


# Routes
@api_bp.route("/zip_upload/", methods=["GET", "POST"])
def zip_upload():
    if request.method == "POST":
        # check if the post request has the file part
        if KM.validate_api_key(request.values.get("api_key")) is False:
            return jsonify({"error": "Invalid API key"}), 400
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
            uploaded_filename = os.path.join(
                current_app.config["UPLOAD_FOLDER"], filename
            )
            file.save(uploaded_filename)
            task = classify_new_zip.delay(uploaded_filename)
            return jsonify({"task_id": task.id}), 202


@api_bp.route("/file_upload/", methods=["POST"])
def file_upload():
    if request.method == "POST":
        # check if the post request has the file part
        if KM.validate_api_key(request.values.get("Invalid API Key")) is False:
            return jsonify({"error": "Missing API Key"}), 400
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not fileselect a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploaded_filename = os.path.join(
                current_app.config["UPLOAD_FOLDER"], filename
            )
            file.save(uploaded_filename)
            task = classify_new_file.delay(uploaded_filename)
            return jsonify({"task_id": task.id}), 202


@api_bp.route("/results/<task_id>", methods=["GET"])
def get_results_file(task_id):
    try:
        return send_file(
            os.path.join(current_app.config["RESULTS_FOLDER"], f"{task_id}.json"),
            attachment_filename=f"{task_id}.json",
        )
    except Exception as e:
        return str(e)


# https://testdriven.io/blog/flask-and-celery/
@api_bp.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)


@api_bp.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    task = create_task.delay(int(task_type))
    return jsonify({"task_id": task.id}), 202


@api_bp.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": str(task_result.result),
    }

    if task_result.status == "SUCCESS":
        results_upload(task_result.result, task_id)
    return jsonify(result), 200
