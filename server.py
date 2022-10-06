from flask import Flask
from rateV1 import rateV1
from flask import render_template, request
app = Flask('app')

# Use this to get access to student data


@app.route('/')
def index():
    rateV1
    return render_template("index.html")



app.run(host='0.0.0.0', port=8080)