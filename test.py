import os
import csv

def get_format_matrix():
    standard_list_path = r'C:\Users\baiwt\Desktop\demo_5.csv'
    with open(standard_list_path) as f:
        reader = csv.reader(f)
        format_matrix = list(reader)
    print(format_matrix)

get_format_matrix()