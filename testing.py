import networkx as nx
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

g = nx.Graph()
g.add_path(['uk', 'france', 'usa'])
pos = nx.spring_layout(g)

fig.set_facecolor('w')
ax.set_axis_off()
nodes = g.nodes()
artist = nx.draw_networkx_nodes(g, pos, ax=ax, nodelist=nodes, node_size=1000)
artist.set_picker(5)
nx.draw_networkx_edges(g, pos, ax=ax)
nx.draw_networkx_labels(g, pos, ax=ax)

def onpick(event):
    artist = event.artist
    mouseevent = event.mouseevent
    print "Click Location:", mouseevent.xdata, mouseevent.ydata
    idx = event.ind[0] 
    print "Node:", nodes[idx]
    print
       
fig.canvas.mpl_connect('pick_event', onpick)
plt.show()
