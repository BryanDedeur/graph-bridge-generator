
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
import math # cos sin pi
import random

from scipy import interpolate

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

    # graph variables
    circle_radius = 4;

    # routing
    tours = []
    robot_colors = ["red", "blue", "green", "orange"]
    offset = 0.15
    edge_visits = []

    ## ------------------------------------------------------- GENERAL FUNCTIONS -------------------------------------------------------- ##

    def make_edge_with_weight(self, v1, v2, weight):
        self.edges.append([v1, v2, weight])

    # makes an edges and computes the weight from the distance between vertices
    def make_edge(self, v1, v2):
        self.edges.append([v1, v2, np.linalg.norm(v1-v2)])

    def make_bridge(self, type_id, segments):
        self.max_segments = segments + 3 # + 3 to add two ends and a middle cross section
        for i in range(self.max_segments):
            self.make_segment(type_id)
    
    ## ----------------------------------------------------------- LOADING ------------------------------------------------------------- ##

    def load_data(self, vertices, edges, weights):
        largest_vertex_index = 0;
        if len(edges) == len(weights):
            for i in range(len(edges)):
                self.make_edge_with_weight(edges[i][0], edges[i][1], weights[i])
                if (edges[i][0] > largest_vertex_index):
                    largest_vertex_index = edges[i][0]
                if (edges[i][1] > largest_vertex_index):
                    largest_vertex_index = edges[i][1]
        if len(vertices) == 0:
            # make a circle graph if no vertices
            radInbetweenVertices = (2 * math.pi) / (largest_vertex_index + 1)
            currentRad = 0;
            for i in range(largest_vertex_index + 1):
                self.vertices.append([self.circle_radius * math.cos(currentRad), self.circle_radius * math.sin(currentRad), 0])
                currentRad += radInbetweenVertices
        else:
            self.vertices = vertices

    def get_edge(self, v1, v2):
        for e in range(len(self.edges)):
            if self.edges[e][0] == v1 and self.edges[e][1] == v2:
                return e
            if self.edges[e][0] == v2 and self.edges[e][1] == v1:
                return e
   
    def load_tours(self, tours):
        self.tours = tours
        # count the number of visits per edge
        for edge in self.edges:
            self.edge_visits.append(0)
        for t in range(len(tours)):
            for v in range(len(tours[t])):
                if v < len(tours[t]) - 1:
                     self.edge_visits[self.get_edge(tours[t][v], tours[t][v + 1])] += 1


    ## ------------------------------------------------------- SEGMENT CREATION -------------------------------------------------------- ##
    def make_single_point_segment(self):
        self.vertices.append([self.segment_length * self.segment_count,0,0])

    # desc: makes a segment of the bridge
    # var1: int bridge_type
    # var2: list of ints last_segment_attachment_vertices
    def make_segment(self, type):
        if type == 0: # pratt
            self.make_pratt_segment()
        self.segment_count += 1

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

    ## ------------------------------------------------------- VISUALIZATIONS -------------------------------------------------------- ##

    def plot_graph(self, ax, annotate_vertices):
        # plot the graph
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
            if annotate_vertices:
                ax.annotate(str(v), (self.vertices[v][0], self.vertices[v][1]))
        ax.scatter(x, y)
        # plot the edges
        for e in range(len(self.edges)):
            x = (self.vertices[self.edges[e][0]][0], self.vertices[self.edges[e][1]][0])
            y = (self.vertices[self.edges[e][0]][1], self.vertices[self.edges[e][1]][1])
            ax.plot(x, y, color="gray")

    def visualize(self):
        # plotting things
        fig, ax = plt.subplots(len(self.tours) + 1, figsize=(4, 8))
        #fig.suptitle('Something')
        for t in range(len(self.tours)):
            self.plot_graph(ax[t], True)
            ax[t].title.set_text('R'+ str(t))
            # plot the tours
            x = []
            y = []
            for v in range(len(self.tours[t])):
                vertex = self.tours[t][v]
                x.append(self.vertices[vertex][0] + random.uniform(-self.offset, self.offset))
                y.append(self.vertices[vertex][1] + random.uniform(-self.offset, self.offset))
                if v < len(self.tours[t]) - 1:
                    # pull the tours close to the edge
                    x.append(self.vertices[vertex][0] + ((self.vertices[self.tours[t][v + 1]][0] - self.vertices[vertex][0]) / 2))
                    y.append(self.vertices[vertex][1] + ((self.vertices[self.tours[t][v + 1]][1] - self.vertices[vertex][1]) / 2))

            f, u = interpolate.splprep([x, y], s=0, per=True)
            #create interpolated lists of points
            xint, yint = interpolate.splev(np.linspace(0, 1, 500), f)
            ax[t].plot(xint, yint, color = self.robot_colors[t])

        # plot the overlap
        ax[len(self.tours)].title.set_text('Overlap')
        self.plot_graph(ax[len(self.tours)], False)
        for i in range(len(self.edge_visits)):
            if self.edge_visits[i] > 1:
                x = (self.vertices[self.edges[i][0]][0], self.vertices[self.edges[i][1]][0])
                y = (self.vertices[self.edges[i][0]][1], self.vertices[self.edges[i][1]][1])
                ax[len(self.tours)].annotate(self.edge_visits[i], ((x[0] + (x[1] - x[0]) / 2), (y[0] + (y[1] - y[0]) / 2)))
                ax[len(self.tours)].plot(x, y, color=(1 - (1/self.edge_visits[i]), .2, .9 - (1/self.edge_visits[i])))


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
