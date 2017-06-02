import math

class Course(object):
    # Attributes and Constructor
    # ============================================
    # Initialization
    # String   name      :
    # String   state     :
    # Course[] parents   :
    # Course[] children  : 
    # ============================================
    def __init__(self, code, state,  parents=[], numRequired, children=[]):
        self.code = code
        self.state = state
        self.prereqs = (parents, numRequired)
        self.children = children
        self.depth = -1 # Uninitialized
        
    # Mutators and Accessors
    def getCode():
        return self.code
    def getState():
        return self.state
    def getPrereqs():
        return self.prereqs
    def getChildren():
        return self.children
    def getDepth(): # This will probably have to change
        if (self.depth == -1):
            if (len(getPrereqs()[0]) == 0):
                self.depth = 0
            self.depth = 1 + max([course.getDepth() for course in getPrereqs()[0]])
        return self.depth
    def setState(newState):
        old = getState()
        self.state = newState
        return old

    # Propogating Up
    def propogate():
        if getDepth() == 0:
            return
        if getState() == 1: # required/selected

            if len(getPrereqs()[0]) == 1:
                getPrereqs()[0][0].setState(1)
                getPrereqs()[0][0].propogate()
            else:
               def propogateMaybe():
                   # should work the same way for if current node's state is maybe
                        
            
    

