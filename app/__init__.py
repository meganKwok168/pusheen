# Pusheen
# Softdev 2026
# P04

from flask import Flask
from flask import render_template
from flask import request
from flask import session, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
