 the OPENAI_API_KEY  and run flask app
<br>

export FLASK_APP={python_file_pyth}
<br>

flask  run --host=0.0.0.0  -p 5000 --no-debugger  --no-reload

<br>

http://127.0.0.1/chat
<br>

<br>
crontab <br>
@reboot /bin/bash /home/ubuntu/chat/start.sh<br>
<br>
*/5 * * * * /bin/bash /home/ubuntu/chat/start.sh<br>

