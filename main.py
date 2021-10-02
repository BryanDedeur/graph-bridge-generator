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

#vertices, edges, weights = load_graph_file("truss-example1.csv")
#vertices = load_obj_file("truss-example.obj")
vertices, edges, weights = load_graph_file("pratt-truss-bridge-4-segment.json")
vertex_routes = load_routes_file("decoded-route-pratt-truss-bridge-4-segment-3R-pops100-200gens-chc-ox-inv.tsv")

bridge = Bridge()
# load or create a bridge
if len(vertices) > 0 or len(edges) > 0:
    bridge.load_data(vertices, edges, weights)
else:
    bridge.make_bridge(BRIDGE_TYPE_ID, SEGMENTS)

# load routes
bridge.load_tours(vertex_routes)
bridge.graph_name = "pratt-truss-bridge-4-segment"

bridge.visualize()










