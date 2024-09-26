# By using split_settings, this code serves the purpose of
# appending all .py codes present in the settings folder
# together for them to run as a whole.
"""
Remember to set up the virtual environment by using venv
or Poetry
"""

import os.path
from pathlib import Path

from split_settings.tools import include, optional

# Gets the project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Namespacing our own custom enviroment variables
ENVVAR_SETTINGS_PREFIX = "CORESETTINGS_"

LOCAL_SETTINGS_PATH = os.getenv(f"{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    "base.py",
    "logging.py",
    "custom.py",
    optional(LOCAL_SETTINGS_PATH),
    "envvars.py",
)
