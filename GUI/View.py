import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

import sys
from PyQt4 import QtGui


class View(object):
    def __init__(self, label_mode):
        self.label_mode = label_mode
    def Display(self, G):
        #plt.title('draw_networkx')
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=False, arrows=False)

        pos_higher = {}
        y_off = -25
        for k, v in pos.items():
            if k in self.label_mode:
                pos_higher[k] = (v[0], v[1] + y_off)
            else:
                pos_higher[k] = (v[0], v[1])



        nx.draw_networkx_labels(G, pos_higher, self.label_mode, font_size=12)
        plt.savefig('nx_test.png')

        nx.get_node_attributes(G, 'color')
