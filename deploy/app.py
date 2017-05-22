from flask import Flask, render_template, redirect, url_for, request, jsonify, json
import sys
import csv

app = Flask(__name__)
app.secret_key = 'imagine-you-are-a-light-molecule...'

state = 'New York'
year = '1977'

@app.route("/", methods = ['GET', 'POST'])
# displays the data visualization
def home():
    return render_template('main.html', info = readStateByYear(state, year), dObj = getInfo(), year = year, state = state)
