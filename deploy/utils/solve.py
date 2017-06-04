#import graph,
import csv
from graph import Course

# Data Parsing From CSV 
# Name, Parents, NumReq, State, Categories, 
raw = open("../static/sample.csv", "r").read().strip().replace("\r\n", "\n").split("\n")
courselist = []
for course in raw:
    c = course.split(",")
    courselist += [ Course(c[0], 
                           0 if c[3] == "" else int(c[3]),
                           int(c[2]),
                           c[4].split("|"),
                           c[1].split("|")) ]
    
for i in courselist:
    print i
