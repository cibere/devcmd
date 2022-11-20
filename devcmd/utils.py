import os
import sys
from io import StringIO


def filter_text(text: str):
    if os.getenv("name"):
        text = text.replace(str(os.getenv("name")), "[MY NAME]")
    return text


class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    async def __aenter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    async def __aexit__(self, type, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io.getvalue()  # type: ignore
