#!/bin/bash
# Start Gunicorn with optimized settings
/home/codespace/test_app/env/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
