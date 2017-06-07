#import graph,
import csv
from graph import Course

# ============================================
# Functions
# ============================================
# Function updating the relative depths of each course
def updateRelDepths(courselist):
    checked = []
    tocheck = [i for i in courselist if i.getState() == 1] # Seeded With Required Nodes
    nextdepth = 0
    while len(tocheck) > 0: 
        tmp = len(tocheck) # Temporary Variable, Easy Degeneration of tocheck
        checked += [tocheck]
        for c in tocheck[:tmp]:
            for child in c.getChildren():
                if child not in tocheck and child.getState() != -1: # Not Required
                    tocheck += [child] # Add Children to List To Be Checked
            c.setRelDepth(nextdepth)
        tocheck = tocheck[tmp:]
        nextdepth += 1
    

# Function taking list of selected coursenames and modifying graph accordingly
def updateGraph(coursenames):
    selected = []
    for course in courselist:
        if course.getName() in coursenames:
            selected.append(course)
    for course in selected:
        course.setState(1)
        course.propogateRequested()

# Function collecting selected/required courses into a list
def selected():
    ret = []
    for course in courselist:
        if course.getState() == 1:
            ret.append(course)
    return ret

def maybes():
    ret = []
    for course in courselist:
        if course.getState() == 2:
            ret.append(course)
    return ret

# Function traversing through graph: mark nodes by propogating selected/required courses, then check grad requirements and mark nodes as "maybe" accordingly.
def traverse():
    # Propagate Upwards For Requested
    selectedCourses = selected() # Requested Courses - State == 1
    for course in selectedCourses:
        print repr(course), "propogating"
        course.propogateRequested() # Propogate Upwards
    for course in selectedCourses: # Adding Requirements
        for cat in course.getCategory():
            categories[cat][0] += 1

    # Debugging
    for course in selected():
        print "required: " + repr(course)

    # Propogate Upwards For Maybes
    maybeCourses = maybes()
    for course in maybeCourses:
        print repr(course), "propogating maybes"
        course.propogateMaybe() # Propogate Upwards - Maybes

    # Add Category Checking Here - TODO

    unfulfilled = {}
    for key, value in categories.items():        
        if value[0] < value[1]:
            unfulfilled[key] = value
    if len(unfulfilled) > 0:
        for category in unfulfilled:
            for course in courselist:
                if course.getState() == 0 and category in course.getCategory():
                    course.setState(2)
                    course.propogateRequested() # classes marked as maybe if grad req isn't fulfilled
    def removeNode(course):
        for parent in course.getParents():
            parent.removeChild(course)
        for child in course.getChildren():
            child.removeParent(course)
        courselist.remove(course)
    for course in courselist:
        if course.getState() == 0:
            removeNode(course) # pruned
    maybeCourses = maybes()
    toAJAX = {}
    if len(unfulfilled) > 0:
        for key, value in unfulfilled.items():
            numNeeded = value[1] - value[0]
            choices = []
            lowestCurrentRelDepth = 0
            while len(choices) < numNeeded:
                lowestCurrentRelDepth += 1
                for course in maybeCourses:
                    # print course
                    if key in course.getCategory() and course.getRelDepth() == lowestCurrentRelDepth:
                        choices.append(course.getName())
                        toAJAX[key] = {'helptext':'Choose ' + numNeeded + ' of the following courses.', 'choices':choices}
                    break

                break
    else:
        generateTree(courselist) # Build Tree
    return toAJAX                        

# ============================================
# Writing to Tree CSV
# ============================================
# Course, Prereq
def generateTree(graph):
    tree = open("../static/tree.csv", "w")
    for node in graph:
        line = node.getName() + "," + node.getParents()[0].getName() + "\n"
        treefile.write(line)
    treefile.close()

# ============================================
# Data Parsing From CSV 
# ============================================
# Name, Parents, NumReq, State, Categories, 
raw = open("../static/test.csv", "r").read().strip().replace("\r\n", "\n").split("\n")[1:] # Debugging
#raw = open("../static/courses.csv", "r").read().strip().replace("\r\n", "\n").split("\n")[1:]
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
        try:
            parents[i] = coursedict[parents[i]]
        except:
            print parents[i], "is not in coursedict."
    coursedict[c].setParents(parents)

# Adding Courses to List for Iteration
for c in coursedict:
    courselist += [coursedict[c]]

# Adding Children to Nodes in courselist Based on Parents
for c in courselist:
    parents = c.getParents()
    for p in parents:
        p.addChild(c)

# Creating List of Categories
categories = {}
for c in courselist:
    cat = c.getCategory()
    for categ in cat:
        if categ not in categories:
            categories[categ] = [0,0] # [requested, required]

# Debugging Categories
categories['Left'][1] = 5
categories['Right'][1] = 3

'''
# Deleting categories from dictionary that are  already fulfilled by preselected mandatory classes            
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

# Populating category dictionary with number of credits needed for each
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
'''

# True Depth Calculation
checked = []
tocheck = [i for i in courselist if len(i.getParents()) == 0] # Seeded with Mother Node
nextdepth = -1
while len(tocheck) > 0: 
    tmp = len(tocheck) # Temporary Variable, Easy Degeneration of tocheck
    checked += [tocheck]
    for c in tocheck[:tmp]:
        for child in c.getChildren():
            if child not in tocheck:
                tocheck += [child] # Add Children to List To Be Checked
        c.setTrueDepth(nextdepth)
    tocheck = tocheck[tmp:]
    nextdepth += 1

# Updating Required Classes
# TO CHANGE 
reqs = open("../static/reqs.csv", "r").read().strip().replace("\r\n", "\n").split("\n")
for i in reqs:
    coursedict[i].setState(1)

# Debugging - Look at Required Courses
'''
for i in coursedict:
    if coursedict[i].getState() == 1:
        print i
'''
# Traverse and Update
traverse()

# Rel Depth Updating - Untested
updateRelDepths(courselist)

# Testing
#for i in coursedict:
#    print str(coursedict[i])
