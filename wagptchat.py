import json
import logging
from flask import Flask, render_template, request,send_from_directory

import os

from pathlib import Path

from revChatGPT.V3 import Chatbot

cur_dir = os.path.abspath(__file__).rsplit(os.path.sep, 1)[0]
parent_dir = os.path.dirname(cur_dir)
app = Flask(__name__)
app.name = 'app'

with open(cur_dir + os.path.sep + 'config.json', "r", encoding="utf-8") as config_file:
            confignow = json.load(config_file)

openaikey=confignow["OPENAI_API_KEY"]



###############################################################################
#
#            获取文件
#
###############################################################################
@app.route('/js/<path:path>')
def getjs(path):
    response = send_from_directory(
        cur_dir + os.path.sep + 'js', path, mimetype='text/javascript')
    return response


@app.route('/css/<path:path>')
def getcss(path):
    response = send_from_directory(
        cur_dir + os.path.sep + 'css', path, mimetype='text/css')
    return response

###############################################################################
#
#             gpt服务
#
###############################################################################
parent_dir = Path(__file__).resolve().parent
chatbot = Chatbot(api_key=openaikey)

def generate_response(prompt):
    try:
        response = chatbot.ask(prompt)
        return response
    except Exception as e:
        return e
    
@app.route("/chat")
def chat():
    chatbot.reset()
    return render_template("chat.html")


@app.route("/chat/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(generate_response(user_text))

# if app.name=='app':
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
