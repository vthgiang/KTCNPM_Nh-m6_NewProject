import networkx as nx
import matplotlib.pyplot as plt
import graphistry
from pylab import *
import pandas as pd
from constant import *
from reader import *

class AnnoteFinder:  # thanks to http://www.scipy.org/Cookbook/Matplotlib/Interactive_Plotting
    """
    callback for matplotlib to visit a node (display an annotation) when points are clicked on.  The
    point which is closest to the click and within xtol and ytol is identified.
    """
    def __init__(self, xdata, ydata, annotes, axis=None, xtol=None, ytol=None):
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None: xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
        if ytol is None: ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
        self.xtol = xtol
        self.ytol = ytol
        if axis is None: axis = gca()
        self.axis= axis
        self.drawnAnnotations = {}
        self.links = []

    def __call__(self, event):
        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
            #print(dir(event),event.key)
            if self.axis is None or self.axis==event.inaxes:
                smallest_x_dist = float('inf')
                smallest_y_dist = float('inf')

                for x,y,a in self.data:
                    # print(clickX, x, clickY, y);
                    if abs(clickX-x) <= RADIUS and abs(clickY-y) <= RADIUS:
                        dx, dy = x - clickX, y - clickY
                        self.drawAnnote(event.inaxes, x, y, a)
    def drawAnnote(self, axis, x, y, annote):
        if (dist_sum[annote] == 0):
            fig1, ax1 = plt.subplots()
            ax1.set_title('Module')
            ax1.plot(dist_all[annote]);
        else:
            fig1, ax = plt.subplots(2)
            ax[0].set_title('Sprint')
            ax[0].plot(dist_all[annote]);
            ax[1].set_title('Cumulative sprint')
            ax[1].plot(dist_sum[annote]);
        plt.show();

dist_all = [0] * 17
dist_sum = [0] * 17

def draw_origin_graph():
    global distribution
    G = read_graph('module_relations.txt')
    color_map = ['black'] * 16
    for i in range(1, 13):
        dist_all[i] = read_dist_from_file("out/dist" + str(i) + ".txt");
    read_result('result.txt', G, color_map, dist_all, dist_sum)
    pos = read_pos('pos.txt')
    options = {
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }
    nx.draw_networkx(G,pos,arrows=True, **options, node_color = color_map)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)
    x, y, annotes = [], [], []
    for key in pos:
        d = pos[key]
        annotes.append(key)
        x.append(d[0])
        y.append(d[1])

    af = AnnoteFinder(x, y, annotes)
    connect('button_press_event', af)
    show()


draw_origin_graph()