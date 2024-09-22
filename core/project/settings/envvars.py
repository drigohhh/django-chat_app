from core.core.utils.collections import deep_update
from core.core.utils.settings import get_settings_from_enviroment

"""
This takes env variables with a matching prefix, strips out the prefix, and adds it to globals

For example:
export CORESETTINGS_IN_DOCKER=TRUE (environment variable)

Could then be referenced as a global as:
IN_DOCKER (where the value would be True)
"""

# globals() is a dictionary of global variables
deep_update(globals(), get_settings_from_enviroment(ENVVAR_SETTINGS_PREFIX))  # type: ignore # noqa: F821
