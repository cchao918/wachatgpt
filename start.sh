#!/bin/bash

if lsof -i :5000 > /dev/null; then
    echo "Flask application is already running."
else
    export FLASK_APP=/home/ubuntu/chat/wagptchat.py
    export FLASK_ENV=production
    nohup flask run --host 0.0.0.0 --port 5000 --no-debugger --no-reload > /dev/null 2>&1 &
    echo "chat application started."
fi

