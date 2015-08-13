import os

themes = {
    "Much Dark. Such goth": "dark.css",
    "Oh my eyes": "eyes.css",
}


def resolve(name):
    f = os.path.join(os.path.dirname(__file__), name)
    return f


def get_theme(name):
    with open(resolve(themes[name])) as f:
        data = f.read()
    return data
