
# ---------------------------------------------
#   Graph Bridge generator
#   Evolutionary Computing Systems Lab 
#   University of Nevada, Reno 
# 
#   Created: 9/4/2020
#   By: Bryan Dedeurwaerder
# ---------------------------------------------

import numpy as np
from numpy import array

class Bridge:
    def __init__(self):
        self.data = []

    # bridge variables
    vertices = []           # index is the vertex id while the value is the vec3 position
    edges = []              # index is the edge id while the value is a vec3 vertex_id1 vertex_id2 weight
    max_segments = 10
    segment_count = 0
    height = 2
    segment_length = 1

    def make_edge(self, vid1, vid2):
        self.edges.append(array([vid1, vid2, np.linalg.norm(vid1-vid2)]))

    def make_single_point_segment(self):
        self.vertices.append(array([self.segment_length * self.segment_count,0,0]))

    # makes a pratt segment
    def make_pratt_segment(self):
        if self.segment_count == 0:
            # make first or last segment
            self.make_single_point_segment()
        else:
            if self.segment_count == self.max_segments - 1:
                self.make_single_point_segment()
            else:
                # make midway segements
                self.vertices.append(array([self.segment_length * self.segment_count, 0, 0]))
                self.vertices.append(array([self.segment_length * self.segment_count, self.height, 0]))

            if self.segment_count == 1:
                self.make_edge(0, len(self.vertices) - 1)
                self.make_edge(0, len(self.vertices) - 2)
                self.make_edge(len(self.vertices) - 1, len(self.vertices) - 2)
            elif self.segment_count == self.max_segments - 1: # the last segment
                self.make_edge(len(self.vertices) - 2, len(self.vertices) - 1)
                self.make_edge(len(self.vertices) - 3, len(self.vertices) - 1)
            elif self.max_segments / self.segment_count > 2: # left half of bridge
                self.make_edge(len(self.vertices) - 2, len(self.vertices) - 1) # vertical
                self.make_edge(len(self.vertices) - 3, len(self.vertices) - 2) # diagonal
                self.make_edge(len(self.vertices) - 4, len(self.vertices) - 2) # lower horizontal
                self.make_edge(len(self.vertices) - 3, len(self.vertices) - 1) # upper horizontal
            elif self.max_segments / self.segment_count < 2: # right half of bridge
                self.make_edge(len(self.vertices) - 2, len(self.vertices) - 1) # vertical
                self.make_edge(len(self.vertices) - 1, len(self.vertices) - 4) # diagonal
                self.make_edge(len(self.vertices) - 4, len(self.vertices) - 2) # lower horizontal
                self.make_edge(len(self.vertices) - 3, len(self.vertices) - 1) # upper horizontal

    # desc: makes a segment of the bridge
    # var1: int bridge_type
    # var2: list of ints last_segment_attachment_vertices
    def make_segment(self, type):
        if type == 0: # pratt
            self.make_pratt_segment()

        self.segment_count += 1

    def make_bridge(self, type_id):
        for i in range(self.max_segments):
            self.make_segment(type_id)

        return



    def clear():
        return
