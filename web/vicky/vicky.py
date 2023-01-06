
import random
import string
import threading

from flask import Blueprint
from flask import session, request
from flask import jsonify, render_template, redirect, url_for

from robot import Robot

from utils.time_utils import get_year_by_date_str, get_month_by_date_str, get_day_by_date_str

vicky_app = Blueprint("vicky", __name__, url_prefix="/vicky")

matrix = {}

@vicky_app.route("")
def deny_308():
    return redirect( url_for("vicky.index") )

@vicky_app.route("/", endpoint="index")
def index():
    global matrix
    session_hash = session.get( "session_hash" )

    if session_hash and session_hash in matrix.keys():
        avatar_url = matrix.get(session_hash).get("bot").state.profile["AVATAR"]
        pic = matrix.get(session_hash).get("bot").state.profile["PIC"]
        user_pic = matrix.get(session_hash).get("user_pic")
        return render_template( "vicky.html", avatar_url=avatar_url, pic=pic, user_pic=user_pic )
    else:
        return redirect( url_for("vicky.profile") )

@vicky_app.route("/profile", endpoint="profile")
def profile():
    return render_template( "profile.html" )

@vicky_app.route("/setting", methods = ["POST"])
def setting_profile():
    global matrix

    session_hash = session.get("session_hash")
    if session_hash is None:
        session_hash = "".join( random.sample(string.ascii_lowercase + string.digits, 11) )
        session["session_hash"] = session_hash

    user = request.form.get("user")
    name = request.form.get("name")
    gender = request.form.get("gender")
    birthday = request.form.get("birthday")
    describe = request.form.get("describe")
    avatar = request.form.get("avatar")
    pic = request.form.get("pic")
    user_pic = request.form.get("user_pic")

    profile = {
        "NAME": name,
        "GENDER": gender,
        "YEAROFBIRTH": str( get_year_by_date_str(birthday) ),
        "MONTHOFBIRTH": str( get_month_by_date_str(birthday) ),
        "DAYOFBIRTH": str( get_day_by_date_str(birthday) ),
        "DESCRIBE": [describe],
        "PIC": pic,
        "AVATAR": avatar
    }
    memory = {}
    memory["history"] = []
    memory["lock"] = threading.Lock()
    memory["user"] = user
    memory["user_pic"] = user_pic
    memory["bot"] = Robot(profile)

    matrix[session_hash] = memory

    return redirect( url_for("vicky.index") )

@vicky_app.route("/writing")
def write():
    return render_template( "writing.html" )

@vicky_app.route("/api_v1/get_session_hash")
def get_session_hash():
    global matrix

    session_hash = session.get("session_hash")
    if session_hash:
        if session_hash in matrix.keys():
            return jsonify({"status": 0, "hash": session_hash})
        else:
            return jsonify({"status": 1, "hash": session_hash})
    else:
        return jsonify({"status": 2})

@vicky_app.route("/api_v1/set_session_hash")
def set_session_hash():
    global matrix

    if request.args.get("hash"):
        session["session_hash"] = request.args.get("hash")

    session_hash = session.get("session_hash")
    if session_hash:
        if session_hash in matrix.keys():
            return jsonify({"status": 0, "hash": session_hash})
        else:
            return jsonify({"status": 1, "hash": session_hash})
    else:
        return jsonify({"status": 2})

@vicky_app.route("/api_v1/get_history")
def get_history():
    global matrix

    session_hash = session.get("session_hash")
    if session_hash:
        memery = matrix.get(session_hash, {})
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

@vicky_app.route("/api_v1/writing", methods=['POST'])
def writing():
    global matrix
    session_hash = session.get("session_hash")
    if not session_hash:
        session_hash = request.args.get("hash")
    memery = matrix.get(session_hash, {})
    prompt = request.form.get("prompt")
    txt = ""
    with memery["lock"]:
        bot = memery["bot"]
        txt = bot.write(prompt)
    return jsonify({"status": 0, "text": txt})

@vicky_app.route("/api_v1/chat")
def send_msg():
    global matrix
    session_hash = session.get("session_hash")
    if not session_hash:
        session_hash = request.args.get("hash")
    memery = matrix.get(session_hash, {})
    with memery["lock"]:
        user = memery["user"]
        bot = memery["bot"]
        history_list = memery["history"]

        if request.args.get("message"):
            input_item = {
                "speaker" : user,
                "message" : request.args.get("message")
            }
        else:
            input_item = {
                "speaker" : user,
                "message" : ""
            }
        output = bot.chat(input_item)
        history_list.append(input_item)
        for item in output:
            history_list.append(item)
            item["type"]="incoming"
        matrix[session_hash]["history"] = history_list

        return jsonify({
            "status" : 0,
            "output" : output
        })
