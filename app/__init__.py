from flask import Flask, render_template, request
from flask import session, redirect
from data import makeGraphic
app = Flask(__name__)

#homepage
@app.route('/', methods=['GET', 'POST'])
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

if __name__ == "__main__":
    app.debug = True
    app.run()
