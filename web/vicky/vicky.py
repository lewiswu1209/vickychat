
import random
import string
import threading

from flask import Blueprint
from flask import session, request
from flask import render_template, redirect, url_for

from robot import Robot
from web.vicky.global_var import matrix
from utils.time_utils import get_year_by_date_str, get_month_by_date_str, get_day_by_date_str

vicky_app = Blueprint("vicky", __name__, url_prefix="/vicky")

@vicky_app.route("")
def deny_308():
    return redirect( url_for("vicky.index") )

@vicky_app.route("/", endpoint="index")
def index():
    session_hash = session.get( "session_hash" )
    if not session_hash:
        session_hash = request.args.get("hash")
        session["session_hash"] = session_hash
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
    session_hash = session.get( "session_hash" )
    if not session_hash:
        session_hash = request.args.get("hash")
    if session_hash and session_hash in matrix.keys():
        return render_template( "writing.html" )
    else:
        return redirect( url_for("vicky.profile") )
