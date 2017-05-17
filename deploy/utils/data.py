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
               (id INTEGER, title TEXT, classcount INTEGER)",
               "CREATE TABLE IF NOT EXISTS connections \
               (id INTEGER, courseid INTEGER, coursename TEXT, coursedesc TEXT, children TEXT, parents TEXT)"]
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

# Database - Data Modification
# ==========================================================================
    
# Helper Functions
# ==========================================================================

# Initialization
# ==========================================================================
if (__name__ == "__main__"):
    try:
        reset()
    except:
        init()
        reset()    
