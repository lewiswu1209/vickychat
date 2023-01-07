
from flask import jsonify
from flask import Blueprint
from flask import session, request

from web.vicky.global_var import matrix

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api_v1")

@api_v1.route("/get_session_hash")
def get_session_hash():
    session_hash = session.get("session_hash")
    if session_hash:
        if session_hash in matrix.keys():
            return jsonify({"status": 0, "hash": session_hash})
        else:
            return jsonify({"status": 1, "hash": session_hash})
    else:
        return jsonify({"status": 2})

@api_v1.route("/set_session_hash")
def set_session_hash():
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

@api_v1.route("/get_history")
def get_history():
    session_hash = session.get("session_hash")
    if not session_hash:
        session_hash = request.args.get("hash")
    if session_hash and session_hash in matrix.keys():
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

@api_v1.route("/writing", methods=['POST'])
def writing():
    session_hash = session.get("session_hash")
    if not session_hash:
        session_hash = request.args.get("hash")
    if session_hash and session_hash in matrix.keys():
        memery = matrix.get(session_hash, {})
        prompt = request.form.get("prompt")
        txt = ""
        with memery["lock"]:
            bot = memery["bot"]
            txt = bot.write(prompt)
        return jsonify({"status": 0, "text": txt})
    else:
        return jsonify({"status": -1, "text": "ERROR"})

@api_v1.route("/chat")
def send_msg():
    session_hash = session.get("session_hash")
    if not session_hash:
        session_hash = request.args.get("hash")
    if session_hash and session_hash in matrix.keys():
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
    else:
        return jsonify({
            "status" : -1,
            "output" : ["error"]
        })
