from ModelTree import ModelTree
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

class LogicalNodes():
    def __init__(self):
        pass
#        self.layer_matr = res
#        self.G = nx.DiGraph()
    def Networkx(self, layer_matr):
        #print layer_matr
        G=nx.DiGraph()
        for c_ in layer_matr:
            for b_ in c_:
                G.add_node(b_)
                l = len(c_)
                for index, b_ in enumerate(c_):
                    if index < (l-1):
                        G.add_edge(b_, c_[index + 1])
        return G
