# ---------------------------------------------
#   Graph Bridge generator
#   Evolutionary Computing Systems Lab 
#   University of Nevada, Reno 
# 
#   Created: 9/4/2020
#   Forked by: Bryan Dedeurwaerder
#   Oiginal Creator: Nicholas Harris
# ---------------------------------------------

import argparse
import pathlib # for getting file extensions
import os.path
from os import path
import json


#Function to parse a boolean value from a string given in the command line arguments
def str_to_bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def load_graph_file(file):
    if not path.exists(file):
        print("File does not exist: " + file)
        quit(0)

    vertices = []
    edges = []
    weights = []
    # determine file type
    file_extension = pathlib.Path(file).suffix
    if (file_extension == ".csv"):
        vertices, edges, weights = load_csv_format(file)
    elif(file_extension == ".json"):
        vertices, edges, weights = load_json_format(file)

    return vertices, edges, weights

def load_csv_format(filepath):
    vertices = []
    edges = []
    weights = []
    file = open(filepath, 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        string_list = lines[i].split(',')
        for j in range(len(string_list)):
            # skip adding same edge twice
            if (j < i):
                continue
            value = float(string_list[j])
            if (value > 0):
                edges.append((i, j))
                weights.append(value)
    file.close()
    return vertices, edges, weights

def load_routes_file(filepath):
    tours = []
    file = open(filepath, 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        string_list = lines[i].split(',')
        tours.append([])
        for j in range(len(string_list)):
            value = int(float(string_list[j]))
            tours[i].append(value)
    file.close()
    return tours


def load_obj_file(filepath):
    vertices = []
    file = open(filepath, 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        string_list = lines[i].split(' ')
        vertices.append([])
        for j in range(len(string_list)):
            if (j == 0):
                if (string_list[j] != 'v'):
                    break
                else:
                    continue;
            value = int(float(string_list[j]))
            vertices[i].append(value)
    file.close()
    return vertices

def load_json_format(filepath):
    vertices = []
    edges = []
    weights = []
    file = open(filepath, 'r')
    data = json.load(file)
    file.close()
    for v in data['vertices']:
        vertices.append([v['v2Pos'][0] , v['v2Pos'][1]])
    for e in data['edges']:
        edges.append([e['vIDs'][0] , e['vIDs'][1]])
        weights.append(e['length'])

    return vertices, edges, weights