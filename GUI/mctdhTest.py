import mctdh

config = mctdh.controlParameters()
config.initialize('/home/piet/Schreibtisch/masterarbeit/Qt-with-Python/GUI/Projects/pro1/ch3/mctdh.config')
basis = mctdh.MctdhBasis()
basis.initialize('/home/piet/Schreibtisch/masterarbeit/Qt-with-Python/GUI/Projects/pro1/ch3/CH3f11.txt', config)


bottom_list = []
mode_list = []
nodes_spf = {}

def getBottomlayer():
    """Get the bottom nodes"""
    for i in range(basis.NmctdhNodes()):
        node = basis.MCTDHnode(i)
        if node.Bottomlayer() == True:
            bottom_list.append(i)
    return bottom_list

print getBottomlayer()

def getPhysCoord():
    """get the Modes of the pys. Coordinates"""
    for i in range(basis.NmctdhNodes()):
        node = basis.MCTDHnode(i)
        if node.Bottomlayer() == True:
            phys = node.phys_coor()
            mode_list.append(phys.mode()) #append Modes to list
    return mode_list

print getPhysCoord()

def get_SPFs():
    """get the SPFs of each Node"""
    for i in range(basis.NmctdhNodes()):
        node = basis.MCTDHnode(i)
        tdim = node.t_dim()
        nodes_spf[i] = tdim.GetnTensor() #dict
    return nodes_spf

print get_SPFs()