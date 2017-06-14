from flask import Flask, render_template, redirect, url_for, request, jsonify, json
import sys
import csv
from utils import course_selector

app = Flask(__name__)
app.secret_key = 'imagine-you-are-a-light-molecule...'

state = 'New York'
year = '1977'

course_selector_courses = course_selector.convert_csv_to_dict()
print course_selector_courses
@app.route("/d3test", methods = ['GET', 'POST'])
# displays the data visualization
def home():
    return render_template('d3.html', csv = f)

@app.route("/class_selector", methods = ['GET'])
def class_selector():
    art_courses = course_selector_courses["Art"]
    bio_courses = course_selector_courses["Biology"]
    chem_courses = course_selector_courses["Chemistry"]
    cs_courses = course_selector_courses["Computer Science"]
    eng_courses = course_selector_courses["English"]
    health_courses = course_selector_courses["Health and Physical Education"]
    math_courses = course_selector_courses["Mathematics"]
    music_courses = course_selector_courses["Music"]
    phys_courses = course_selector_courses["Physics"]
    social_courses = course_selector_courses["Social Studies"]
    tech_courses = course_selector_courses["Technology"]
    return render_template('class_selector.html')

if __name__ == "__main__":
    app.debug = True
    app.run()


