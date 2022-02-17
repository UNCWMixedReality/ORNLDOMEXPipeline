import os


class DevelopmentConfig:
    TESTING = False
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = os.path.join(
        os.getcwd(), os.environ.get("UPLOAD_FOLDER", "uploads")
    )
    RESULTS_FOLDER = os.path.join(
        os.getcwd(), os.environ.get("RESULTS_FOLDER", "results")
    )
    API_KEYS = os.environ.get("API_KEYS", "test")


class TestingConfig:
    UPLOAD_FOLDER = os.path.join(
        os.getcwd(), os.environ.get("UPLOAD_FOLDER", "uploads")
    )
    RESULTS_FOLDER = os.path.join(
        os.getcwd(), os.environ.get("RESULTS_FOLDER", "results")
    )
    API_KEYS = os.environ.get("API_KEYS", "test")
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
