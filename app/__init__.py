from flask import Flask, render_template, request, jsonify
from flask import session, redirect, url_for, flash
import sqlite3, os
from data import makeGraphic
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "aevfiyawvfgwuga"

# DB_FILE = "database.db"

client = MongoClient("mongodb://localhost:27017")
mongo = client["database"]

# def setup_database():
#     db = sqlite3.connect(DB_FILE)
#     c = db.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             username TEXT PRIMARY KEY,
#             password TEXT,
#             session_key TEXT,
#             login_token TEXT
#         );
#     """)
#     db.commit()
#     db.close()

# setup_database()

#login
# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == 'POST':
#         db = sqlite3.connect(DB_FILE)
#         c = db.cursor()
#         username = request.form["username"]
#         password_form = request.form["password"]
#         c.execute("SELECT password FROM users WHERE username = ?", (username,))
#         user_data = c.fetchone()
#         db.close()
#         if user_data:
#             passworddb = user_data[0]
#             if password_form == passworddb:
#                 session["username"] = username
#                 return redirect(url_for('index'))
#             else:
#                 flash("Incorrect password. Try again.")
#         else:
#             flash("Username incorrect or not found. Try again.")
#         return redirect(url_for('login'))
#     return render_template('login.html')

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        userData = mongo.users.find_one({"_id": username}, {"password":1})
        if userData:
            if password == userData["password"]:
                session["username"] = username
                return redirect(url_for('index'))
            else:
                flash("Incorrect password. Try again.")
        else:
            flash("Username incorrect or not found. Try again.")
        return redirect(url_for('login'))
    return render_template('login.html')

#createaccount
# @app.route("/createaccount", methods = ['GET', "POST"])
# def set_user():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = sqlite3.connect(DB_FILE)
#         c = db.cursor()
#         c.execute("SELECT * FROM users WHERE username = ?", (username,))
#         user_exists = c.fetchone()
#         if user_exists:
#             db.close()
#             flash("Username already taken!")
#             return redirect(url_for('set_user'))
#         c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         db.commit()
#         db.close()
#         session['username'] = username
#         return redirect(url_for('index'))
#     return render_template('createaccount.html')

@app.route("/createaccount", methods = ['GET', "POST"])
def set_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if mongo.users.find_one({"_id": username}):
            flash("Username already taken!")
            return redirect(url_for('set_user'))
        mongo.users.insert_one({
            "_id": username,
            "password": password
        })
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('createaccount.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('login.html')

#main
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

#handling data
@app.route('/data')
def getGraphic():
    limit=request.args.get('limit')
    metric = request.args.get('metric')
    specification = request.args.get('specification')
    data = makeGraphic(limit, specification, metric)
    return render_template("data.html", graph=data, Metric = metric, Specification = specification, Limit=limit)

@app.route('/api/data')
def getGraphicData():
    limit = request.args.get('limit')
    metric = request.args.get('metric')
    specification = request.args.get('specification')
    data = makeGraphic(limit, specification, metric)
    return jsonify(data)

if __name__ == "__main__":
    app.debug = True
    app.run()
