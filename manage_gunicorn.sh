#!/bin/bash
ACTION=$1

if [[ $ACTION == "start" ]]; then
    echo "Starting Gunicorn..."
    ~/test_app/env/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
elif [[ $ACTION == "stop" ]]; then
    echo "Stopping Gunicorn..."
    pkill gunicorn
elif [[ $ACTION == "restart" ]]; then
    echo "Restarting Gunicorn..."
    pkill gunicorn
    ~/test_app/env/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
elif [[ $ACTION == "status" ]]; then
    pgrep -a gunicorn && echo "Gunicorn is running" || echo "Gunicorn is not running"
else
    echo "Usage: $0 {start|stop|restart|status}"
fi
