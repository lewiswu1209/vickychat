
import json
import threading

from flask import jsonify
from flask import Blueprint
from flask import session, request

from robot import Robot
from web.vicky.global_var import matrix
from utils.time_utils import get_day_by_date_str
from utils.time_utils import get_year_by_date_str
from utils.time_utils import get_month_by_date_str

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api_v1")

@api_v1.route("/<id>/write", methods=['POST'])
def write(id):
    if id in matrix.keys():
        unit = matrix.get(id, {})
        prompt = request.form.get("prompt")
        txt = ""
        with unit["lock"]:
            bot = unit["bot"]
            txt = bot.write(prompt)
        return jsonify({
            "code": 0,
            "msg": "success",
            "data": {
                "generated_text": txt,
                "full_text": "{}{}".format(prompt, txt)
            }
        })
    else:
        return jsonify({
            "code": 101,
            "msg": "bot dos not exist"
        })

@api_v1.route("/<id>/chat")
def chat(id):
    if id in matrix.keys():
        unit = matrix.get(id, {})
        with unit["lock"]:
            bot = unit["bot"]

            if request.args.get("speaker"):
                if request.args.get("message"):
                    input_item = {
                        "speaker" : request.args.get("speaker"),
                        "message" : request.args.get("message")
                    }
                else:
                    input_item = {
                        "speaker" : request.args.get("speaker"),
                        "message" : ""
                    }
                output = bot.chat(input_item)
                for item in output:
                    item["type"]="incoming"

                return jsonify({
                    "code": 0,
                    "msg": "success",
                    "data": {
                        "len": len(output),
                        "response": output
                    }
                })
            else:
                return jsonify({
                    "code": 201,
                    "msg": "who are you?"
                })
    else:
        return jsonify({
            "code": 101,
            "msg": "bot dos not exist"
        })
