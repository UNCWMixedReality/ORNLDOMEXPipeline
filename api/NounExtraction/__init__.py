import os
from pathlib import Path

from flask import Flask


def create_app(test_config=None):
    from .api import api_bp  # noqa: E402

    UPLOAD_FOLDER = os.path.join(
        os.getcwd(), os.environ.get("UPLOAD_FOLDER", "uploads")
    )

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.path.join(app.instance_path, "NounExtraction.sqlite"),
        UPLOAD_FOLDER=UPLOAD_FOLDER,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
