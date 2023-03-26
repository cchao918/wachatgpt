import os
import openai
import json


cur_dir = os.path.abspath(__file__).rsplit(os.path.sep, 1)[0]
parent_dir = os.path.dirname(cur_dir)
with open(cur_dir + os.path.sep + 'config.json', "r", encoding="utf-8") as config_file:
    confignow = json.load(config_file)
openaikey = confignow["OPENAI_API_KEY"]
username = confignow['USERNAME']
password = confignow['PASSWORD']
maxmsgcount = int(confignow['MAXMSG_COUNT'])
initengine = confignow['ENGINE']
prompt = confignow['PROMPT']

openai.organization = "org-XZy7m6GKxNH7JBJUcw73p0L2"
openai.api_key = openaikey
print(openai.Model.list())

