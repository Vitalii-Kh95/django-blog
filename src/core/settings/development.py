from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.2", "192.168.0.112"]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = (
    "https://localhost:3000/",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://192.168.1.2:5173",
    "http://192.168.0.112:5173",
)

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:3000/",
    "http://localhost:5173",
    "http://192.168.1.2:5173",
    "http://192.168.0.112:5173",
]

# django toolbar settings
INTERNAL_IPS = ["127.0.0.1"]
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",  # Optional: Customize the date format
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": str(LOGS_DIR / "django_error.log"),
        },
        "request_response_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": str(LOGS_DIR / "request_response.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,  # Prevent duplication by stopping propagation to the root logger
        },
        "request_response": {
            "handlers": ["request_response_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],  # Handles logs not covered by specific loggers
        "level": "WARNING",  # Set higher level to reduce noise
    },
}
