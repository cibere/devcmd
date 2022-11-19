import os


def filter_text(text: str):
    if os.getenv("name"):
        text = text.replace(str(os.getenv("name")), "[MY NAME]")
    return text
