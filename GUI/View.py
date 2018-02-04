import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

import sys
from PyQt4 import QtGui


class View(object):
    def __init__(self):
        pass
    def Display(self, G):
        #plt.title('draw_networkx')
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True, arrows=False)
        plt.savefig('nx_test.png')
