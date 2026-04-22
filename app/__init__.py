from flask import Flask, render_template, request, jsonify
from flask import session, redirect, url_for, flash
from data import makeGraphic
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "aevfiyawvfgwuga"

client = MongoClient("mongodb://localhost:27017")
mongo = client["database"]

#login
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
    return redirect(url_for('login'))

#main
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

#handling data
@app.route('/data')
def getGraphic():
    limit1=request.args.get('limit1')
    limit2=request.args.get('limit2')
    metric = request.args.get('metric')
    specification = request.args.get('specification')
    data = makeGraphic(limit1, limit2, specification, metric)
    return render_template("data.html", graph=data, Metric = metric, Specification = specification, Limit1=limit1,Limit2=limit2)

@app.route('/api/data')
def getGraphicData():
    limit1 = request.args.get('limit1')
    limit2 = request.args.get('limit2')
    metric = request.args.get('metric')
    specification = request.args.get('specification')
    data = makeGraphic(limit1, limit2, specification, metric)
    return jsonify(data)

if __name__ == "__main__":
    app.debug = True
    app.run()
