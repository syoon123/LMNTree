import math



class Course(object):
    # Attributes and Constructor
    # ============================================
    # Initialization
    # String   name      : 
    # Course[] parents   :
    # Course[] children  : 
    # ============================================
    def __init__(self, name, parents=[], children=[]):
        self.name = name
        # self.desc = [Do we need this?]
        self.parents = parents
        self.children = children
        self.depth = -1 # Uninitialized
        
    # Mutators and Accessors
    def getParents():
        return self.parents
    def getChildren():
        return self.children
    def getDepth():
        if (self.depth == -1):
            if (len(getParents()) == 0):
                self.depth = 0
            self.depth = 1 + max([course.getDepth() for course in getParents()])
        return self.depth 

