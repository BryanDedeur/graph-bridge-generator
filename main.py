# ---------------------------------------------
#   Graph Bridge generator
#   Evolutionary Computing Systems Lab 
#   University of Nevada, Reno 
# 
#   Created: 9/4/2020
#   This Fork by: Bryan Dedeurwaerder
#   Oiginal Creator: Nicholas Harris
# ---------------------------------------------

from helpers import *
from bridge import *
import sys, getopt


BRIDGE_NAME = "bridge"
GRAPH_FILE = ""
COORD_FILE = ""
BRIDGE_TYPE_ID = 0      # [0] pratt [1] parker [2] k-truss [3] howe {the truss structure}
SEGMENTS = 4            # [0] 10 segment bridge {the number of repeating sections along the length of the bridge}
VERTICES_CAP = 0        # [0] no cap [>0] capped {the bridge will stop generating when we hit this number of vertices}
EDGES_CAP = 0           # [0] no cap [>0] capped {the bridge will stop generating when we hit this number of edges}
ONE_SIDED = True
THREE_DIM = False       # [false] will output 2D coordinates [true] will output 3D coordinates

def usage():
    print("TODO")

def parse_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v:g:", ["help", "graph", "coords"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-g", "--graph"):
            GRAPH_FILE = a
        elif o in ("--coords"):
            COORD_FILE = a
        else:
            continue
    return 0

parse_args()


bridge = Bridge()
if GRAPH_FILE != "":
    bridge.load(GRAPH_FILE, COORD_FILE)
bridge.make_bridge(BRIDGE_TYPE_ID, SEGMENTS)
bridge.visualize()










