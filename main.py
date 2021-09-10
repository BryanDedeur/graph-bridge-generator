# ---------------------------------------------
#   Graph Bridge generator
#   Evolutionary Computing Systems Lab 
#   University of Nevada, Reno 
# 
#   Created: 9/4/2020
#   This Fork by: Bryan Dedeurwaerder
#   Oiginal Creator: Nicholas Harris
# ---------------------------------------------

import sys
from helpers import *
from bridge import *

BRIDGE_NAME = "bridge"
BRIDGE_TYPE_ID = 0      # [0] pratt [1] parker [2] k-truss [3] howe {the truss structure}
SEGMENTS = 4            # [0] 10 segment bridge {the number of repeating sections along the length of the bridge}
VERTICES_CAP = 0        # [0] no cap [>0] capped {the bridge will stop generating when we hit this number of vertices}
EDGES_CAP = 0           # [0] no cap [>0] capped {the bridge will stop generating when we hit this number of edges}
ONE_SIDED = True
THREE_DIM = False       # [false] will output 2D coordinates [true] will output 3D coordinates

#read arguments passed from command line
def parse_args():
#    NUM_VERTICES =  if len(sys.argv) > 0 : int(sys.argv[1])  
#    DENSITY =       0.0     if len(sys.argv) > 1     else float(sys.argv[2])
#    WINDY =         False   if len(sys.argv) > 2     else str_to_bool(sys.argv[3])
#    MAKE_BRIDGE =   True    if len(sys.argv) > 3     else str_to_bool(sys.argv[4])
#    OUTPUT_FILE =   "graph" if len(sys.argv) > 4     else sys.argv[5]
    return 0

parse_args()

bridge = Bridge()
bridge.make_bridge(BRIDGE_TYPE_ID, SEGMENTS)
bridge.visualize()








