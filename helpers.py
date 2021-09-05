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