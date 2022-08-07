from flask import Flask

poetry_factory = Flask(__name__)

from poetry_factory import routes
