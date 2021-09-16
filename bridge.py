
# ---------------------------------------------
#   Graph Bridge generator
#   Evolutionary Computing Systems Lab 
#   University of Nevada, Reno 
# 
#   Created: 9/4/2020
#   By: Bryan Dedeurwaerder
# ---------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

from numpy import array
from mpl_toolkits.mplot3d import Axes3D

class Bridge:
    def __init__(self):
        self.data = []

    # bridge variables
    vertices = []           # index is the vertex id while the value is the vec3 position
    edges = []              # index is the edge id while the value is a vec3 vertex_id1 vertex_id2 weight
    max_segments = 2        # better if a even number
    segment_count = 0
    height = 2
    segment_length = 1
    type_name = "Pratt"

    def make_edge(self, vid1, vid2):
        self.edges.append([vid1, vid2, np.linalg.norm(vid1-vid2)])

    def make_single_point_segment(self):
        self.vertices.append([self.segment_length * self.segment_count,0,0])

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
                self.vertices.append([self.segment_length * self.segment_count, 0, 0])
                self.vertices.append([self.segment_length * self.segment_count, self.height, 0])

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
            elif self.max_segments / self.segment_count <= 2: # right half of bridge
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

    def make_bridge(self, type_id, segments):
        self.max_segments = segments + 3 # + 3 to add two ends and a middle cross section
        for i in range(self.max_segments):
            self.make_segment(type_id)

    def visualize(self):
        # plotting things
        fig = plt.figure(figsize=(4,4))
        ax = fig.add_subplot(111)
        #plt.autoscale(False)

        #fig.suptitle((str(self.max_segments - 3) + ' Segment ' + self.type_name), fontsize=14)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])

        # plot the vertices
        x = []
        y = []
        for v in range(len(self.vertices)):
            x.append(self.vertices[v][0])
            y.append(self.vertices[v][1])
            ax.annotate(str(v), (self.vertices[v][0], self.vertices[v][1]))

        #ax.scatter(x, y)

        # plot the edges
        for e in range(len(self.edges)):
            x = []
            x.append(self.vertices[self.edges[e][0]][0])
            x.append(self.vertices[self.edges[e][1]][0])
            y = []
            y.append(self.vertices[self.edges[e][0]][1])
            y.append(self.vertices[self.edges[e][1]][1])
            ax.plot(x, y, color="gray")

        plt.show()

    def visualize3D(self):
        # plotting things
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111, projection='3d')

        #fig.suptitle((str(self.max_segments - 3) + ' Segment ' + self.type_name), fontsize=14)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        ax.axes.zaxis.set_visible(False)

        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        ax.axes.zaxis.set_ticklabels([])


        #plt.autoscale(False)
        #ax.auto_scale_xyz([0, 10], [0, 1], [0, 1])
        # ax.set_xlim3d(0, 10)
        # ax.set_ylim3d(0, 2)
        # ax.set_zlim3d(0, 2) 

        # plot the vertices
        x = []
        y = []
        z = []
        for v in range(len(self.vertices)):
            x.append(self.vertices[v][2])
            y.append(self.vertices[v][0])
            z.append(self.vertices[v][1])

        # scaling the plot

        x_scale=1
        y_scale=self.max_segments
        z_scale=self.height

        max_scale=max(x_scale, y_scale, z_scale)

        x_scale=x_scale/max_scale
        y_scale=y_scale/max_scale
        z_scale=z_scale/max_scale


        scale=np.diag([x_scale, y_scale, z_scale, 1.0])
        scale=scale*(1/scale.max())
        scale[3,3]=1

        def short_proj():
          return np.dot(Axes3D.get_proj(ax), scale)

        ax.get_proj=short_proj

        ax.scatter(x, y, z)


        # plot the edges
        for e in range(len(self.edges)):
            x = []
            x.append(self.vertices[self.edges[e][0]][2])
            x.append(self.vertices[self.edges[e][1]][2])
            y = []
            y.append(self.vertices[self.edges[e][0]][0])
            y.append(self.vertices[self.edges[e][1]][0])
            z = []
            z.append(self.vertices[self.edges[e][0]][1])
            z.append(self.vertices[self.edges[e][1]][1])
            ax.plot(x, y, z, color="gray")

        plt.show()
        #plt.savefig('common_labels.png', dpi=300)
        #print(save directory)



    def clear():
        return
