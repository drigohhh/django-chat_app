import os.path

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def printApi():
    if OPENAI_API_KEY:  # type: ignore  # noqa: F821
        print(os.environ["OPENAI_API_KEY"])  # type: ignore # noqa: F821
