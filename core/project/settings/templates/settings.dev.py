# CLONE THIS INTO A 'local/' FOLDER, THIS IS JUST A TEMPLATE

# Template for the Local Settings file
# You can add more settings to override Django's
# default settings or add your own enviroment
# variables, as this will also work as a .env file

DEBUG = True
SECRET_KEY = ""

# These variables SHOULD be located on your virtual enviroment
# if you are using Poetry
os.environ["OPENAI_API_KEY"] = ""  # type: ignore  # noqa: F821

LOGGING["formatters"]["colored"] = {  # type: ignore  # noqa: F821
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}

LOGGING["loggers"]["core"]["level"] = "DEBUG"  # type: ignore  # noqa: F821
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # type: ignore  # noqa: F821
LOGGING["handlers"]["console"]["formatter"] = "colored"  # type: ignore  # noqa: F821
