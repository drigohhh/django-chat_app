# Template for the Local Settings file
# You can add more settings to override Django's
# default settings

DEBUG = True
SECRET_KEY = ""

LOGGING["formatters"]["colored"] = {  # type: ignore  # noqa: F821
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}

LOGGING["loggers"]["core"]["level"] = "DEBUG"  # type: ignore  # noqa: F821
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # type: ignore  # noqa: F821
LOGGING["handlers"]["console"]["formatter"] = "colored"  # type: ignore  # noqa: F821
