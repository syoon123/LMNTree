import csv, os
DIR = os.path.dirname('__file__') + "/"
def convert_csv_to_dict():
    f = open(DIR + "/utils/data/StuyCourses.csv")
    dict = {}
    for line in f.readlines():
        list_of_classes = line.split(",")[1:]
        dict[line.split(",")[0]] = list_of_classes
    return dict
    
