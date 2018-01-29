import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

class View(object):
    def __init__(self):
        self.G = nx.DiGraph()
    def Networkx(self):
        G=nx.DiGraph()
        for c_ in layer_matr:
            for b_ in c_:
                G.add_node(b_)
                l = len(c_)
                for index, b_ in enumerate(c_):
                    if index < (l-1):
                        G.add_edge(b_, c_[index + 1])

# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
#        write_dot(G,'test.dot')

# same layout using matplotlib with no labels
        plt.title('draw_networkx')
        pos =graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True, arrows=False)
        plt.savefig('nx_test.png')
