import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

import sys
from PyQt4 import QtGui


class View(object):
    def __init__(self, label_mode, nodes_spf):
        self.label_mode = label_mode
        self.nodes_spf = nodes_spf
        self._G = nx.DiGraph()
    def Display(self, G):
        #plt.title('draw_networkx')
        top = ['Top']
        rest_nodes = [l_ for l_ in self.nodes_spf.keys() if l_ not in self.label_mode.keys()]
        #print G.edges(data=True)
        #G[2][0]['weight'] = 1
        #G[2][1]['weight'] = 1
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=False, arrows=False, node_color='w')
        nx.draw_networkx_nodes(G, pos, nodelist=top, node_color='w', alpha=1)
        nx.draw_networkx_nodes(G, pos, nodelist=rest_nodes, node_color='r', alpha=1)

        pos_lower = {}
        x_off = 0
        y_off = -5
        for k, v in pos.items():
            pos_lower[k] = (v[0] + x_off, v[1] + y_off)

        nx.draw_networkx_labels(G, pos_lower, self.label_mode, font_size=16)

        pos_higher = {}
        x_off = -7
        y_off = 27
        for k, v in pos.items():
            pos_higher[k] = (v[0] + x_off, v[1] + y_off)
#            if k in self.label_mode:
#                pos_higher[k] = (v[0], v[1] + y_off)
#            else:
#                pos_higher[k] = (v[0], v[1])

        nx.draw_networkx_labels(G, pos_higher, self.nodes_spf, font_size=12)
        plt.savefig('nx_test.png')
        plt.clf()

        for key, ele_ in self.nodes_spf.items():
            G.nodes[key]["SPF"] = ele_
        for key, ele_ in self.label_mode.items():
            G.nodes[key]["Mode"] = ele_
        self._G = G
#        print self.label_mode
#        print self.nodes_spf
    #    nx.get_node_attributes(G, 'color')
#        print G.successors('Top').next()


    if __name__ == '__main__':
        pass
