#import graph,
import csv

# Data Parsing From CSV 
# NAME,PREREQ1|..|PREREQN,CATEGORY1|..|CATEGORYN\n
raw = open("../static/sample.csv", "r").read().strip().split(",")
courselist = { Course(c[0], 

print raw


