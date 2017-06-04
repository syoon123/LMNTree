#import graph,
import csv
from graph import Course

# Data Parsing From CSV 
# Name, Parents, NumReq, State, Categories, 
raw = open("../static/sample.csv", "r").read().strip().replace("\r\n", "\n").split("\n")
courselist = []
coursedict = {}
# Generating Dictionary of Courses
for course in raw:
    c = course.split(",")
    coursedict[c[0]] = Course(c[0],
                              0 if c[3] == "" else int(c[3]),                                                        int(c[2]),
                              [] if c[4] == "" else c[4].split("|"),
                              [] if c[1] == "" else c[1].split("|"))

# Replacing Prereqs With Courses, Not Coursenames
for c in coursedict:
    parents = coursedict[c].getParents()
    for i in range(len(parents)):
        parents[i] = coursedict[c]
    coursedict[c].setParents(parents)

# Adding Courses to List for Iteration
for i in coursedict:
    courselist += [coursedict[i]]

# Testing
for i in coursedict:
    print coursedict[i]
for i in courselist:
    print i
