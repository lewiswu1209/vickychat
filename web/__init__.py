
import os

from flask import Flask
from datetime import timedelta

from web.vicky.vicky import vicky_app
from web.vicky.api_v1.api_v1 import api_v1

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(45)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

vicky_app.register_blueprint(api_v1)
app.register_blueprint(vicky_app)
