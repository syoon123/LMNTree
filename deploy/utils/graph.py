import math

class Course(object):
    # Attributes and Constructor
    # ============================================
    # Initialization
    # String   name      :
    # int      state     :
    # String[] category  :    
    # Course[] parents   :
    # Course[] children  :
    # int numRequired    :
    # int depth          :
    # ============================================
    def __init__(self, name, state, numRequired, category=[], parents=[]): # Not sure if numRequired is actually necessary
        self.name = name
        self.state = state
        self.category = category
        self.children = [] # Unpopulated - Remove If Unneeded
        self.prereqs = [parents, numRequired]
        self.truedepth = 0 # Uninitialized
        self.reldepth = 0 # Updated Only For Traversals

    def __str__(self):
        return "Name: " + self.name + "\nParents: " + ", ".join([repr(i) for i in self.getParents()]) + "\nChildren: " + ", ".join([repr(i) for i in self.getChildren()]) + "\nCategories: " + ", ".join([cat for cat in self.category]) + "\nTrue Depth: " + str(self.truedepth) + "\nRel Depth: " + str(self.reldepth) + "\n"

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
    def getTrueDepth(self):
        return self.truedepth
    def getRelDepth(self):
        return -1
    def getState(self):
        return self.state

    def setState(self,newState):
        old = self.getState()
        self.state = newState
        return old
    def setParents(self,parents):
        self.prereqs[0] = parents
    def setTrueDepth(self,depth):
        self.truedepth = depth;
    def setRelDepth(self,depth):
        self.reldepth = depth;

    def removeChild(self,child):
        self.children.remove(child)
    def removeParent(self,parent):
        self.prereqs[0].remove(parent)
    def addChild(self, child):
        self.children += [child]
    # Propogating Up
    '''def propogate(self):
        if self.getTrueDepth() == 0:
            return
        elif self.getTrueDepth() == 1:
            for parent in self.getParents():
                if parent.getState() != 1:
                    parent.propogate()'''

    def propogate(self):
        if self.getTrueDepth() == 0:
            return
        if self.getState() == 1: 
            if len(self.getPrereqs()[0]) == 1:
                self.getPrereqs()[0][0].setState(1)
                self.getPrereqs()[0][0].propogate()
            else:
                self.propogateMaybe()
        elif self.getState() == 2:
            self.propogateMaybe()
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
            



