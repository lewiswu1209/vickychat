
import os
import random
import string
import threading

from datetime import timedelta
from flask import Flask, session, request, jsonify, render_template, redirect

from bot.chatbot import Chatbot
from bot.disposition import Disposition

from utils.time_utils import get_year_by_date, get_month_by_date, get_day_by_date

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(74)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

matrix = {}

@app.route("/")
def index() -> str:
  return "Hello world!"

@app.route( "/vicky", methods = ["GET"] )
def chitchat() -> str:
    hash = session.get( "session_hash" )

    if hash and hash in matrix.keys():
        return render_template( "chat_template.html" )
    else:
        return redirect("/vicky/setting")

@app.route( "/vicky/setting", methods = ["GET"] )
def setting() -> str:
    return render_template( "setting_template.html" )

@app.route( "/vicky/api_v1/hash", methods = ["GET"] )
def hash() -> str:
    global matrix

    if request.args.get("hash"):
        session["session_hash"] = request.args.get("hash")

    hash = session.get("session_hash")
    if hash and hash in matrix.keys():
        return jsonify({"status": "success", "hash": hash})
    else:
        return jsonify({"status": "no hash"})

@app.route( "/vicky/api_v1/history", methods = ["GET"] )
def get_history() -> str:
    global matrix

    hash = session.get("session_hash")
    if hash:
        memery = matrix.get(hash, {})
        with memery["lock"]:
            history_list = memery["history"]
            history = []
            for item in history_list:
                if item["speaker"] == memery["user"]:
                    item["type"] = "outgoing"
                else:
                    item["type"] = "incoming"
                history.append(item)
            return jsonify(history)
    else:
        return jsonify([])

@app.route( "/vicky/api_v1/setting", methods = ["POST"] )
def setting_profile() -> str:
    global matrix

    hash = session.get("session_hash")
    if hash is None:
        hash = "".join( random.sample(string.ascii_lowercase + string.digits, 11) )
        session["session_hash"] = hash

    user = request.form.get("user")
    name = request.form.get("name")
    gender = request.form.get("gender")
    birthday = request.form.get("birthday")
    describe = request.form.get("describe")

    profile = {
        "NAME": name,
        "GENDER": gender,
        "YEAROFBIRTH": str( get_year_by_date(birthday) ),
        "MONTHOFBIRTH": str( get_month_by_date(birthday) ),
        "DAYOFBIRTH": str( get_day_by_date(birthday) ),
        "DESCRIBE": [describe]
    }
    memory = {}
    memory["history"] = []
    memory["lock"] = threading.Lock()
    memory["user"] = user
    memory["bot"] = Chatbot(profile, Disposition.ELEGANT)

    matrix[hash] = memory

    return redirect("/vicky")

@app.route( "/vicky/api_v1/chat", methods = ["GET"] )
def chat() -> str:
    global matrix
    hash = session.get("session_hash")
    if hash:
        memery = matrix.get(hash, {})
        with memery["lock"]:
            user = memery["user"]
            bot = memery["bot"]
            history_list = memery["history"]

            if request.args.get("text"):
                input_item = {
                    "speaker" : user,
                    "message" : request.args.get("text")
                }
                output = bot.chat(input_item, history_list)
                history_list.append(input_item)
                history_list.append(output)
                matrix[hash]["history"] = history_list
                output["type"]="incoming"
                return jsonify(output)
    else:
        return jsonify({
            "type": "incoming",
            "message": "我脑子瓦特了~"
        })

def main() -> None:
    app.run( host = "127.0.0.1", port = 18376 )

if __name__ == "__main__":
    main()
