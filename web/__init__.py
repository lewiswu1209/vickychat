
import os

from flask import Flask
from datetime import timedelta

from web.vicky import vicky_app

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(45)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

app.register_blueprint(vicky_app)
