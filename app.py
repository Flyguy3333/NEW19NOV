import sys

# Force Python to use the virtual environment's site-packages
sys.path.insert(0, "/home/codespace/test_app/env/lib/python3.12/site-packages")

# Debug sys.path to ensure the correct paths are prioritized
print("Updated sys.path:", sys.path)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is working with updated sys.path!"

if __name__ == "__main__":
    app.run()
