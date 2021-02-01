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
        list_node = list(G.nodes())
        index = list_node.index(annote)
        if (dist_sum[index] == 0):
            fig1, ax = plt.subplots()
            ax.set_title('Module ' + str(annote) + ' : Completion time distribution')
            ax.plot(dist_all[index])
            ax.set_xlabel('Time ')
            ax.set_ylabel('Probability')
        else:
            fig1, ax = plt.subplots(2)
            ax[0].set_title('Sprint ' + str(annote) + ' : Completion time distribution')
            ax[0].plot(dist_all[index])
            ax[0].set_xlabel('Time')
            ax[0].set_ylabel('Probability')
            ax[1].set_title('Completion time from start to end of Sprint ' + str(annote) + ' :');
            ax[1].plot(dist_sum[index])
            ax[1].set_xlabel('Time')
            ax[1].set_ylabel('Probability')
            plt.tight_layout()
        plt.show();

dist_all = []
dist_sum = []
G = nx.Graph()

def draw_origin_graph():
    global distribution, G, dist_sum, dist_all
    G = read_graph('module_relations.txt')
    color_map = ['black'] * len(G.nodes())
    dist_all = [0] * (len(G.nodes()) + 1)
    dist_sum = [0] * (len(G.nodes()) + 1)
    for i in range(1, 13):
        dist_all[i] = read_dist_from_file("out/dist" + str(i) + ".txt");
    read_result('result_group.txt', 'result_dist.txt', G, color_map, dist_all, dist_sum)
    pos = read_pos('pos.txt')
    options = {
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }
    fig, ax = plt.subplots(figsize=(12, 12))
    # Title/legend
    font = {"fontname": "Helvetica", "color": "k", "fontweight": "bold", "fontsize": 14}
    ax.set_title("The graph of module relations and sprint relations\n(Modules have the same color are belong to the sprint which has that color)", font)
    nx.draw_networkx(G, pos, arrows=True, **options, node_color = color_map, label = 'Concurrent module relations')
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