
import json
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

@vicky_app.route("/user/setting", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        profile_url:str = url_for("vicky.profile")
        session["next"] = request.args.get("next")
        return render_template( "profile.html", profile_url=profile_url )
    if request.method == "POST":
        session["user"] = request.form["user"]
        session["user_pic"] = request.form["user_pic"]
        return redirect( session["next"] )

@vicky_app.route("/<id>")
@vicky_app.route("/<id>/")
@vicky_app.route("/<id>/chatroom")
def chatroom(id):
    if "user" not in session:
        return redirect(url_for("vicky.profile", next=request.full_path))
    if id not in matrix.keys():
        return redirect(url_for("vicky.setting", id=id))
    avatar_url = matrix.get(id).get("bot").state.profile["AVATAR"]
    pic = matrix.get(id).get("bot").state.profile["PIC"]
    user_pic = session["user_pic"]
    chat_api_url = url_for("vicky.api_v1.chat", id=id, speaker=session["user"])
    return render_template( "vicky.html", avatar_url=avatar_url, pic=pic, user_pic=user_pic, chat_api_url=chat_api_url )

@vicky_app.route("/<id>/setting", methods=["GET", "POST"])
def setting(id):
    if request.method == "GET":
        return render_template( "setting.html", setting_url=url_for("vicky.setting", id=id) )
    if request.method == "POST":
        pic      = request.form.get("pic")
        name     = request.form.get("name")
        avatar   = request.form.get("avatar")
        gender   = request.form.get("gender")
        birthday = request.form.get("birthday")
        describe = request.form.get("describe")
        print( request.form.get("examples") )
        examples = json.loads(request.form.get("examples"))
        print( examples)

        profile = {
            "NAME": name,
            "GENDER": gender,
            "YEAROFBIRTH": str( get_year_by_date_str(birthday) ),
            "MONTHOFBIRTH": str( get_month_by_date_str(birthday) ),
            "DAYOFBIRTH": str( get_day_by_date_str(birthday) ),
            "DESCRIBE": [describe],
            "PIC": pic,
            "AVATAR": avatar,
            "EXAMPLES": examples
        }
        unit = {}
        unit["lock"] = threading.Lock()
        unit["bot"] = Robot(profile)

        matrix[id] = unit

        return redirect(url_for("vicky.chatroom", id=id))

@vicky_app.route("/<id>/write")
def write(id):
    write_api_url:str = url_for("vicky.api_v1.write", id=id)
    return render_template( "writing.html", write_api_url=write_api_url )
