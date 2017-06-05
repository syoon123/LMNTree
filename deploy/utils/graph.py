import math

class Course(object):
    # Attributes and Constructor
    # ============================================
    # Initialization
    # String   name      :
    # int      state     :
    # String[] category  :    
    # String[] parents   :
    # String[] children  :
    # int numRequired    :
    # int depth          :
    # ============================================
    def __init__(self, name, state, numRequired, category=[], parents=[]): # Not sure if numRequired is actually necessary
        self.name = name
        self.state = state
        self.category = category
        self.children = [] # Unpopulated - Remove If Unneeded
        self.prereqs = [parents, numRequired]
        self.truedepth = -1 # Uninitialized
        self.reldepth = -1 # Updated Only For Traversals

    def __str__(self):
        return "Name: " + self.name + "\nParents: " + ", ".join([repr(i) for i in self.getParents()]) #+ "\nChildren: " + ", ".join([repr(i) for i in self.getChildren()])

    def __repr__(self):
        return "COURSE " + self.name
        
    # Mutators and Accessors
    def getName(self):
        return self.name
    def getState(self):
        return self.state
    '''
    0: unmarked
    1: required/selected
    2: maybe
    '''
    def getPrereqs(self):
        return self.prereqs
    def getParents(self):
        return self.prereqs[0]
    def getChildren(self):
        return self.children    
    def getCategory(self):
        return self.category
    # Deprecated 
    def getTrueDepth(self): # This will probably have to change
        if (self.truedepth == -1):
            if (len(self.getPrereqs()[0]) == 0):
                self.truedepth = 0
            else:
                self.truedepth = 1 + max([0] + [course.getTrueDepth() for course in self.getPrereqs()[0]])
        return self.truedepth
    def getRelDepth(self):
        return -1

    def setState(self,newState):
        old = getState()
        self.state = newState
        return old
    def setParents(self,parents):
        self.prereqs[0] = parents
    def removeChild(self,child):
        self.children.remove(child)
    def removeParent(self,parent):
        self.prereqs[0].remove(parent)
    def addChild(self, child):
        self.children += [child]
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
            



