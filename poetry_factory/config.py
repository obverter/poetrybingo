import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


def relpath(file):
    print(os.path.join(ROOT_DIR, file))
    return