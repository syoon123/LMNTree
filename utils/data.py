# ========================================
# Database Module
# ========================================

import sqlite3, random

# ==========================================================================
# Database connect()
# precond: database is not open
# postcond: connects to database and returns the database object
# ==========================================================================
def connect():
    name = "./data/data.db" # Change
    db = sqlite3.connect(name)
    return db

# ==========================================================================
# void disconnect(Database db)
# precond: database is open
# postcond: takes a database object, saves it, and closes it
# ==========================================================================
def disconnect(db):
    db.commit()
    db.close()

# Table Initialization Functions
# ==========================================================================
# void init() 
# precond:
# postcond: creates tables in database if they don't already exist
# ==========================================================================
def init():
    db = connect()
    c = db.cursor()
    # Creating Tables
    cmdlist = ["CREATE TABLE IF NOT EXISTS graphlist \
               (graphid INTEGER, title TEXT, classcount INTEGER)",
               "CREATE TABLE IF NOT EXISTS connections \
               (graphid INTEGER, courseid INTEGER, coursename TEXT, coursedesc TEXT, children TEXT, parents TEXT)"]
    for cmd in cmdlist:
        c.execute(cmd)
    disconnect(db)

# ==========================================================================
# void reset()
# precond: tables in database exist (init() has been previously called)
# postcond: clears all entries in the database
# ==========================================================================
def reset():
    db = connect()
    c = db.cursor()
    # Delete Entries
    tablelist = []
    for table in tablelist:
        cmd = "DELETE FROM %s"%(table)
        c.execute(cmd)
    disconnect(db)
    
# Database - Data Addition
# ==========================================================================
def add_graph(name):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO graphlist \
               VALUES (%d, %s, %d)"%(largest_graphid(), name, 0)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

def add_connection(gid, name, desc, children, parents):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO connections \
               VALUES (%d, %d, %s, %s, %s, %s)"%(gid, largest_courseid(gid), name,
                                                 desc, children, parents)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

# Database - Data Modification
# ==========================================================================
    
# Helper Functions
# ==========================================================================
def largest_graphid():
    db = connect()
    c = db.cursor()
    req = "SELECT graphid FROM graphlist"
    data = c.execute(req)
    maxGID = 0
    for entry in data:
        if entry[0] > maxGID:
            maxGID = entry[0]
    disconnect(db)
    return maxGID

def largest_courseid(gid):
    db = connect()
    c = db.cursor()
    req = "SELECT courseid FROM connections WHERE graphid == %d"%(gid)
    data = c.execute(req)
    maxCID = 0
    for entry in data:
        if entry[0] > maxCID:
            maxCID = entry[0]
    disconnect(db)
    return maxCID

def graph_exists(gid):
    return largest_graphid() >= gid

def course_exists(cid, gid):
    return graph_exists(gid) and largest_courseid(gid) >= cid

# Initialization
# ==========================================================================
if (__name__ == "__main__"):
    try:
        reset()
    except:
        init()
        reset()    
