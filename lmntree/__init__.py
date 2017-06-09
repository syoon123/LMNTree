from flask import Flask, render_template, redirect, url_for, request, jsonify, json
import sys
import csv
from utils import course_selector, solve

app = Flask(__name__)
app.secret_key = 'imagine-you-are-a-light-molecule...'

state = 'New York'
year = '1977'
DIR = os.path.dirname('__init__.py')
DIR += '/'
f = open('static/tree.csv','r').read()
course_selector_courses = course_selector.convert_csv_to_dict()
@app.route("/d3test", methods = ['GET', 'POST'])
# displays the data visualization
def home():
    return render_template('d3.html', csv = f)

@app.route("/", methods = ['GET'])
def class_selector():
    art_courses = course_selector_courses["Art"]
    bio_courses = course_selector_courses["Biology"]
    chem_courses = course_selector_courses["Chemistry"]
    cs_courses = course_selector_courses["Computer Science"]
    eng_courses = course_selector_courses["English"]
    health_courses = course_selector_courses["Health and Physical Education"]
    math_courses = course_selector_courses["Mathematics"]
    phys_courses = course_selector_courses["Physics"]
    social_courses = course_selector_courses["Social Studies"]
    tech_courses = course_selector_courses["Technology"]
    return render_template('class_selector.html', art_courses = art_courses, bio_courses = bio_courses, chem_courses= chem_courses, cs_courses = cs_courses, eng_courses = eng_courses, health_courses = health_courses, math_courses = math_courses, phys_courses = phys_courses, social_courses = social_courses, tech_courses = tech_courses)

@app.route("/class_selector_check", methods = ["POST"])
def class_selector_check():
    res = request.json
    classes = res["classes"]
    print classes
    return solve.traverse(classes)

@app.route("/debug/", methods=["GET", "POST"])
def debug():
    reqs = ["G","L"]
    return solve.traverse(reqs)

if __name__ == "__main__":
    app.debug = True
    app.run()


