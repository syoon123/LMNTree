import math

class Course(object):
    # Attributes and Constructor
    # ============================================
    # Initialization
    # String   code      :
    # String   state     :
    # String[] category  :    
    # Course[] parents   :
    # int numRequired    :
    # Course[] children  :
    # int depth          :
    # ============================================
    def __init__(self, code, state, category, parents=[], numRequired, children=[]):
        self.code = code
        self.state = state
        self.category = category
        self.prereqs = (parents, numRequired)
        self.children = children
        self.depth = -1 # Uninitialized
        
    # Mutators and Accessors
    def getCode(self):
        return self.code
    def getState(self):
        return self.state
    '''
    0: unmarked
    1: required/selected
    2: maybe
    '''
    def getPrereqs(self):
        return self.prereqs
    def getChildren(self):
        return self.children
    def getDepth(self): # This will probably have to change
        if (self.depth == -1):
            if (len(getPrereqs()[0]) == 0):
                self.depth = 0
            self.depth = 1 + max([course.getDepth() for course in getPrereqs()[0]])
        return self.depth
    def setState(self,newState):
        old = getState()
        self.state = newState
        return old

    # Propogating Up
    def propogate(self):
        def propogateMaybe(self):            
            count = 0
            for parent in self.getPrereqs()[0]:
                if parent.getState() == 1:
                    parent.propogate()
                    count += 1
            if count == 0:
                for parent in self.getPrereqs()[0]:
                    parent.setState(2)
                    parent.propogate()
        if self.getDepth() == 0:
            return
        if self.getState() == 1: 
            if len(self.getPrereqs()[0]) == 1:
                self.getPrereqs()[0][0].setState(1)
                self.getPrereqs()[0][0].propogate()
            else:
                self.propogateMaybe()
        elif self.getState() == 2:
            self.propogateMaybe()
            



