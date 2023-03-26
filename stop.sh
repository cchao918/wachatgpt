#!/bin/bash

if lsof -i :5000 > /dev/null; then
    kill $(lsof -t -i :5000)
    echo "chat application stopped."
else
    echo "chat application is not running."
fi
