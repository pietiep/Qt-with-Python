from ModelTree import ModelTree
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

class LogicalNodes():
    def __init__(self, layer_matr):
        self.G = nx.DiGraph()
        self.layer_matr = layer_matr
#        self.G = nx.DiGraph()
        self.Networkx()

    def Networkx(self):
        #print layer_matr
        #self.G=nx.DiGraph()
        for c_ in self.layer_matr:
            for b_ in c_:
                self.G.add_node(b_)
                l = len(c_)
                for index, b_ in enumerate(c_):
                    if index < (l-1):
                        self.G.add_edge(b_, c_[index + 1])




#        return G

if __name__ == '__main__':

    model = ModelTree()
    logical = LogicalNodes(model.lay_matr_mode)
