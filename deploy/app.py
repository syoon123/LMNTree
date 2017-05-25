from flask import Flask, render_template, redirect, url_for, request, jsonify, json
import sys
import csv

app = Flask(__name__)
app.secret_key = 'imagine-you-are-a-light-molecule...'

state = 'New York'
year = '1977'

f = open("static/sample.csv").read()

@app.route("/d3test", methods = ['GET', 'POST'])
# displays the data visualization
def home():
    return render_template('d3.html', csv = f)
if __name__ == "__main__":
    app.debug = True
    app.run()
