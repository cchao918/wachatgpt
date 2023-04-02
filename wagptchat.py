import json
import logging
from flask import Flask, render_template, request, send_from_directory, session, redirect
import secrets
import os
from pathlib import Path
from revChatGPT.V3 import Chatbot
import openai
import pickle
import requests
import threading

cur_dir = os.path.abspath(__file__).rsplit(os.path.sep, 1)[0]
parent_dir = os.path.dirname(cur_dir)

app = Flask(__name__)
app.name = 'chat'

with open(cur_dir + os.path.sep + 'config.json', "r", encoding="utf-8") as config_file:
    confignow = json.load(config_file)

app.secret_key = secrets.token_hex(16)
openaikey = confignow["OPENAI_API_KEY"]
username = confignow['USERNAME']
password = confignow['PASSWORD']
maxmsgcount = int(confignow['MAXMSG_COUNT'])
initengine = confignow['ENGINE']
prompt = confignow['PROMPT']

 


###############################################################################

# 获取文件

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


@app.route('/img/<path:path>')
def getimg(path):
    response = send_from_directory(
        cur_dir + os.path.sep + 'img', path, mimetype='image/jpg')
    return response

###############################################################################

# 登录

###############################################################################


@app.route('/')
def root():
    if session.__contains__('username') and session.__contains__('password') and session['username'] == username and session['password'] == password:
        return redirect('/chat')
    # 构建HTML页面
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>登录</title>
        <style>
            /* 居中样式 */
            .center {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            /* 移动端样式 */
            @media only screen and (max-width: 1000px) {
                form {
                    width: 80%;
                }

                label {
                    display: block;
                    margin-bottom: 10px;
                    font-size:200%
                }

                input[type="text"],
                input[type="password"],
                input[type="submit"] {
                    width: 100%;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    margin-bottom: 10px;
                    font-size:200%
                }
            }
        </style>
    </head>
    <body>
        <div class="center">
            <form method="post" action="/login">
                <label>用户名:</label>
                <input type="text" name="username">
                <br><br>
                <label>密码:</label>
                <input type="password" name="password">
                <br><br>
                <input type="Submit" value="登录">
            </form>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/login', methods=['POST'])
def login():
    # 获取表单数据
    username_input = request.form['username']
    password_input = request.form['password']

    # 验证用户名和密码
    if username_input == username and password_input == password:
        # 认证成功，保存用户名到session
        session['username'] = username_input
        session['password'] = password_input
        # # 连接到OpenAI API
        # openai.api_key = openaikey
        # # 为该用户创建一个唯一的会话 ID
        # session['session_id'] = secrets.token_hex(16)
        # # 创建一个新的Chatbot实例并将其存储在会话中
        # chatbot = Chatbot(api_key=openaikey)
        # serialized_chatbot = pickle.dumps(chatbot)
        # session['chatbot'] = serialized_chatbot
        return redirect('/chat')
    else:
        # 认证失败，返回错误信息
        return '用户名/密码错误'

###############################################################################

# gpt服务

###############################################################################



def  getbalance():
    try:
        url = 'https://api.openai.com/dashboard/billing/credit_grants'
        # headers = {'Authorization': 'Bearer ' + openaikey}
        headers = {'Authorization': 'Bearer ' + openaikey ,'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            grant_amount = data['grants']['data'][0]['grant_amount']
            used_amount = data['grants']['data'][0]['used_amount']
            available_amount = grant_amount - used_amount
            return available_amount
        else:
            return -1 
    
    except Exception as e:
        return -1 

parent_dir = Path(__file__).resolve().parent
# chatbot = Chatbot(api_key=openaikey)
chatbot = Chatbot(api_key=openaikey, engine=initengine,system_prompt=prompt)

#强化角色
def createrole():
    try:
        chatbot.ask(prompt)
    except Exception as e:
        try:
            chatbot.ask(prompt)
        except Exception as e:
            try:
                chatbot.ask(prompt)
            except Exception as e:
                try:
                    chatbot.ask(prompt)
                except Exception as e:
                    pass

t = threading.Thread(target=createrole, args=())
t.name = 'create_role'
t.start()

def generate_response(prompt):
    # 获取该用户的Chatbot实例
    # serialized_chatbot = session.get('chatbot')
    # chatbot = pickle.loads(serialized_chatbot)
    # if chatbot is None:
    #     # 如果没有Chatbot实例，则认为用户未登录或会话已过期
    #     return '请先登录'
    try:
        # 使用该用户的Chatbot实例来生成响应
        response = chatbot.ask(prompt)
        return response
    except Exception as e:
        return e

@app.route("/chat")
def chat():
    if not (session.__contains__('username') and session.__contains__('password') and session['username'] == username and session['password'] == password):
        return redirect('/')

    # balance = round(getbalance(),2)
    balance = 0
    return render_template("chat.html", balance=balance,maxmsgcount=maxmsgcount)

@app.route("/chat/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(generate_response(user_text))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)