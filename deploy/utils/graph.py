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
    def __init__(self, name, state,  parents=[], children=[]):
        self.name = name
        self.state = state
        self.parents = parents
        self.children = children
        self.depth = -1 # Uninitialized
        
    # Mutators and Accessors
    def getParents():
        return self.parents
    def getChildren():
        return self.children
    def getDepth(): # Is this necessary anymore?
        if (self.depth == -1):
            if (len(getParents()) == 0):
                self.depth = 0
            self.depth = 1 + max([course.getDepth() for course in getParents()])
        return self.depth 

