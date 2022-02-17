import os
from pathlib import Path

from flask import Flask, render_template


def create_app(script_info=None):
    from .api import api_bp  # noqa: E402

    # create and configure the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    @app.route("/")
    def home():
        return render_template("main/home.html")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    app.shell_context_processor({"app": app})

    return app
