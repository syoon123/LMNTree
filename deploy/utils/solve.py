#import graph,
import csv
from graph import Course

# Data Parsing From CSV 
# Name, Parents, NumReq, State, Categories, 
raw = open("../static/sample2.csv", "r").read().strip().replace("\r\n", "\n").split("\n")
courselist = []
coursedict = {}
# Generating Dictionary of Courses
for course in raw:
    c = course.split(",")
    coursedict[c[0]] = Course(c[0],
                              int(c[3]), 
                              int(c[2]),
                              [] if c[4] == "" else c[4].split("|"),
                              [] if c[1] == "" else c[1].split("|"))
    
# Replacing Prereqs With Courses, Not Coursenames
for c in coursedict:
    parents = coursedict[c].getParents()
    for i in range(len(parents)):
        parents[i] = coursedict[c]
    coursedict[c].setParents(parents)

# Adding Courses to List for Iteration
for c in coursedict:
    courselist += [coursedict[c]]

# Creating List of Categories
categories = {}
for c in courselist:
    cat = c.getCategory()
    for categ in cat:
        if categ not in categories:
            categories[categ] = [0,0] # [requested, required]

# Already fulfilled by preselected mandatory classes            
del categories['FreshBio']
del categories['FreshComp']
del categories['SophChem']
del categories['JuniorPhysics']
del categories['Health']
del categories['EuroLit']
del categories['ArtApp']
del categories['MusicApp']
del categories['Drafting']
del categories['IntroCS1']
del categories['Trig']

# Populate category dictionary with number of credits needed for each
categories['5tech'][1] = 1
categories['USH'][1] = 2
categories['BritLit'][1] = 1
categories['Gov'][1] = 1
categories['Math'][1] = 8
categories['SciElective'][1] = 2
categories['Econ'][1] = 1
categories['10tech'][1] = 2
categories['AmericanLit'][1] = 1
categories['PE'][1] = 8
categories['Geo'][1] = 2
categories['Language'][1] = 6
categories['JuniorEnglish'][1] = 1
categories['SeniorEnglish'][1] = 1
categories['Global'][1] = 4

# DEPRECATED
# True Depth Calculation
# for c in courselist: 
#     c.getTrueDepth()

# Updating With Graduation Requirements
# TODO

# Testing
for i in coursedict:
    print repr(coursedict[i])
for i in courselist:
    print i
for i in categories:
    print i
