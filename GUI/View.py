import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class View(object):
    def __init__(self):
        pass
    def Display(self, G):
        #plt.title('draw_networkx')
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True, arrows=False)
        #plt.savefig('nx_test.png')
        ax = Figure().add_subplot(111)
        ax.clear()
        FigureCanvas(Figure()).draw()
