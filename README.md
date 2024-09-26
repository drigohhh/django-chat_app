# Project setup

Basic chat_app with OpenAI with the Langchain API
(still in wip stage)

Project setup instructions here.

Clone the settings.dev.py into a local folder that you can set your own settings for the logger and your specific secret Django key.

`mkdir -p local`
`cp .\core\project\settings\templates\settings.dev.py .\local\settings.dev.py`

You gotta have [Poetry](https://python-poetry.org/) installed to run this project.

Run `make update` in the terminal and it should install the dependencies and automatically migrate the database.
