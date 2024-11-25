#!/bin/bash
# Kill processes using port 5000
lsof -t -i :5000 | xargs -r kill -9
echo "Port 5000 cleaned up!"
