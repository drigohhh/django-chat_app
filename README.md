# Project Setup

Basic chat app with the OpenAI Langchain API using Django for the Python backend.

## Instructions

### Prerequisites

- [Poetry](https://python-poetry.org/)
- Python 3.10 or higher
- Git

### Steps

1. **Clone the repository:**

```bash
git clone https://github.com/drigohhh/django-chat_app
cd django-chat_app
```

2. **Copy the `settings.dev.py` into a local folder.**

```bash
# Windows
mkdir local
copy .\core\project\settings\templates\settings.dev.py .\local\settings.dev.py
```

```bash
# Linux
mkdir local
cp ./core/project/settings/templates/settings.dev.py ./local/settings.dev.py
```

If this doesn't work, just create the folder 'local' at the top of your environment and copy the file manually.

3. **Install Poetry**

```bash
python -m pip install poetry
```

Poetry will automatically create the virtual environment; be sure to activate it in your IDE.

4. **Set your API key in the environment variable**

In your local settings, set your OpenAI API key for the application to work.

```python
os.environ["OPENAI_API_KEY"] = ""  # type: ignore  # noqa: F821
```

This variable should be located in the environment that Poetry just created. **Make sure** that your code is running from that environment.

5. **Run the Makefile command to install the dependencies and automatically migrate the database.**

```bash
make update
```

6. **Host the server using the command below, and you are good to go!**

```bash
make runserver
```

## Known Bugs

- **Python 3.13 seems to break the installation of some dependencies.**
