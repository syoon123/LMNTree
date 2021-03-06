import csv, json, os
from graph import Course

# ============================================
# Constants
# ============================================

ROOT = os.path.dirname(__file__) + '/..'
TREEPATH = ROOT + "/static/tree.csv"
COURSEPATH = ROOT + "/static/stuy_courses.csv"
TESTPATH = ROOT + "/static/test.csv"
REQPATH = ROOT + "/static/reqs.csv"

# ============================================
# Functions
# ============================================
# Function updating the relative depths of each course
def updateRelDepths(courselist):
    #print "I was called."
    checked = []
    tocheck = [i for i in courselist if i.getState() == 1] # Seeded With Required Nodes
    # print "seed", tocheck # Debugging
    nextdepth = 0
    for c in tocheck:
        c.setRelDepth(nextdepth) # 0
    while len(tocheck) > 0: 
        #print tocheck, len(tocheck) # Debugging
        #print checked # Debugging
        tmp = len(tocheck) # Temporary Variable, Easy Degeneration of tocheck
        for c in tocheck[:tmp]:
            checked += [c]
            for child in c.getChildren():
                if child not in tocheck and child.getState() != 1: # Not Required
                    tocheck += [child] # Add Children to List To Be Checked
            c.setRelDepth(nextdepth)
            # print repr(c), "depth set to", c.getRelDepth() # Debugging
        #print "After iterating through tocheck, ", checked # Debugging
        tocheck = tocheck[tmp:]
        #print tocheck # Debugging
        nextdepth += 1    

# Function taking list of selected coursenames and modifying graph accordingly
def updateGraph(coursenames):
    selected = []
    for course in courselist:
        if course.getName() in coursenames:
            selected.append(course)
    for course in selected:
        course.setState(1)
        course.propagateRequested()

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

# Function to prune all nodes of a category not marked required
def prune(category):
    for course in courselist:
        if category in course.getCategory() and course.getState() == 0: # Maybe Error Here?
            print "pruned", repr(course)
            course.setState(3) # Pruned State
def pruneMaybes(category):
    for course in courselist:
        if category in course.getCategory() and course.getState() == 2: # Maybe
            print "pruned maybe", repr(course)
            course.setState(3) # Pruned State

# Function traversing through graph: mark nodes by propagating selected/required courses, then check grad requirements and mark nodes as "maybe" accordingly.
def traverse(reqs=[]):
    # Updating Required Classes
    for i in reqs:
        coursedict[i.strip()].setState(1)

    # Propagate Upwards For Requested
    selectedCourses = selected() # Requested Courses - State == 1
    for course in selectedCourses:
        print repr(course), "propagating"
        course.propagateRequested() # Propagate Upwards
    # Propagate Upwards For Maybes
    maybeCourses = maybes()
    for course in maybeCourses:
        print repr(course), "propagating maybes"
        course.propagateMaybe() # Propagate Upwards - Maybes

    # Debugging
    for course in selected():
        print "required: " + repr(course)

    # Updating Requirements
    for course in courselist:
        if course.getState() == 2 or course.getState() == 1:
            for cat in course.getCategory():
                categories[cat][0] += 1

    # Category Checking
    unfulfilled = []
    fulfilled = []
    for key, value in categories.items():
        if value[0] < value[1]: # Requested < Required
            unfulfilled += [key]
        else:
            fulfilled += [key]

    print "Unfulfilled:", unfulfilled # Debugging Categories
    print "Fulfilled:", fulfilled # Debugging Categories

    for category in fulfilled:
        prune(category) # Pruning Unmarked Ones

    # Using Relative Depth To Add Courses
    toAJAX = {}
    for category in unfulfilled:
        print "I have moved on to a new category:", category
        check = []
        print "Number to beat:", categories[category][1] # Debugging
        smallestRelDepth = 0
        while (categories[category][0] < categories[category][1]): # Requested < Required
            print categories[category][0] # Debugging
            updateRelDepths(courselist) # Update Relative Depths
            smallestRelDepth += 1
            for c in courselist:
                if category in c.getCategory() and c.getRelDepth() <= smallestRelDepth and c.getState() % 2 != 1: # First Layer, Not 1 (Required) or 3 (Pruned)
                    check += [c]
                    if c.getState() != 2:
                        categories[category][0] += 1
                        c.setState(2) # Make Unmarked Maybe
                    if categories[category][0] < categories[category][1]: # Still Less Than Req'd
                        c.setState(1) # Make First Layer All Required
                        check = []
                        continue
            # print category, "layer", check # Debugging
            if len(check) == 1: # Only One Choice
                check[0].setState(1) # Require The Class
            elif len(check) > 1: # User Will Have To Make A Choice
                toAJAX[category] = [[c.getName() for c in check], len(check) - categories[category][0] + categories[category][1]] # [[items], number_to_select]
            check = [] # The Final Result Will Be The Last Layer
            
    retAJAX = {}
    if len(toAJAX) > 0: # At Least One Unfulfilled Category
        retAJAX["choices"] = toAJAX
        retAJAX["errcode"] = 1 # 1 - Needs User Input
        retAJAX["errmsg"] = "Select more classes!"
    else:
        retAJAX["errcode"] = -1
        retAJAX["errmsg"] = "All is well!"
        print "Final Classes: " + ", ".join([c.getName() for c in courselist if c.getState() == 1 or c.getState() == 2]) # Debugging
        
        # Final Pruning Before Generating Tree
        for c in courselist:
            if c.getName() == "Mother Node":
                c.setState(1)
            if c.getState() == 0:
                c.setState(3) # Make All Unmarked Into Pruned
        prunelist = [c for c in coursedict if coursedict[c].getState() == 3]
        for c in courselist: # Removing From Parents And Children
            c.setParents(filter(
                lambda course : course.getName() not in prunelist, c.getParents()
            ))
            c.setChildren(filter(
                lambda course : course.getName() not in prunelist, c.getChildren()
            ))
        finallist = [c for c in courselist if c.getName() not in prunelist]
        for pc in prunelist:
            del coursedict[pc]

        # Generating Tree
        generateTree(finallist, TREEPATH)
    print json.dumps(retAJAX) # Debugging
    return json.dumps(retAJAX) # Final JSON

# ============================================
# Writing to Tree CSV
# ============================================

# Function taking outputted graph from traverse and name of csv file, populating a tree by duplicating nodes, and writing new graph to the csv
def generateTree(graph, treefile):
    coursetree = [] # basically a new courselist, without cycles

    # keeping track of how many duplicate nodes there are for each course, so names differentiated in csv by number of spaces afterward

    addedToTree = {'Mother Node': 0}
    for node in graph:
        if not (node == None):
            addedToTree[node.getName()] = 0

    # Recursive Function taking a node, its parent, and the tree to be populated, creating nodes to add to courseree
    def createChildNodes(node, parent, tree):
        addedToTree[node.getName()] += 1
        addSelf = Course(node.getName() + (" " * addedToTree[node.getName()]), node.getState(), 1, [], [parent])
        tree.append(addSelf)
        for child in node.getChildren():
            addedToTree[child.getName()] += 1
            if child in node.getParents():                
                newNode = Course(child.getName() + (" " * addedToTree[child.getName()]), child.getState(), 1, [], [addSelf])
                tree.append(newNode)
                continue
            if len(child.getChildren()) == 0:
                newNode = Course(child.getName() + (" " * addedToTree[child.getName()]), child.getState(), 1, [], [addSelf])
                tree.append(newNode)
            else:
                createChildNodes(child, addSelf, tree)

    #Calling createChildNodes, starting with Mother Node (root)
    createChildNodes(graph[0], None, coursetree)
    for i in coursetree:
        print i

    # Going through coursetree and writing to treefile
    f = open(treefile, "w")
    f.write("Course,Prereq,State\n")
    for course in coursetree:
        if course.getName() == "Mother Node ":
            line = course.getName() + ",\n"
        else:
            # print course, course.getState() # Debugging
            line = course.getName() + "," + course.getParents()[0].getName() + "," + str(course.getState()) + "\n"        
        # print line # Debugging
        f.write(line)
    f.close()
    print "wrote to file"
        
# ============================================
# Data Parsing From CSV 
# ============================================
# Name, Parents, NumReq, State, Categories, 
raw = open(TESTPATH, "r").read().strip().replace("\r\n", "\n").split("\n")[1:] # Debugging
#raw = open(COURSEPATH, "r").read().strip().replace("\r\n", "\n").split("\n")[1:]
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

# Adding Children to Nodes in Graph Based on Parents
def populateChildren(courselist):
    for c in courselist:
        parents = c.getParents()
        for p in parents:
            if not (p == None):
                p.addChild(c)

populateChildren(courselist)

# Creating List of Categories
categories = {}
for c in courselist:
    cat = c.getCategory()
    for categ in cat:
        if categ not in categories:
            categories[categ] = [0,0] # [requested, required]

# Debugging Categories

categories['Left'][1] = 5
categories['Right'][1] = 8
'''
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

# Debugging - Look at Required Courses
'''
for i in coursedict:
    if coursedict[i].getState() == 1:
        print i
'''

# Traverse and Update - Testing
if __name__ == "__main__":
    reqs = open(REQPATH, "r").read().strip().replace("\r\n", "\n").split("\n")
    print traverse(reqs)
    print "THIS IS A TEST."
