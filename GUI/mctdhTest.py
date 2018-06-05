import mctdh,sys

config = mctdh.controlParameters()
config.initialize('/home/piet/Schreibtisch/masterarbeit/Qt-with-Python/GUI/Projects/Project1/tmp/mctdh.config')
basis = mctdh.MctdhBasis()
basis.initialize('/home/piet/Schreibtisch/masterarbeit/Qt-with-Python/GUI/Projects/Project1/tmp/a8.txt', config)

nodes_spf = {}
sumBottomNode = {}
sumTopNode = {}
sumPerNode = {}
maxNodes = basis.NmctdhNodes()
remnantNodeList = []

def get_SPFs():
    SumTopNode = 0
    remnantNode = 0

    for i in range(maxNodes):
        node = basis.MCTDHnode(i)
        tdim = node.t_dim()
        nodes_spf[i] = tdim.GetnTensor() 

    mode_spf = {i: basis.MCTDHnode(i).t_dim().active(0) for i in \
                range(maxNodes) if \
                basis.MCTDHnode(i).Bottomlayer() == True}
                
    for key in mode_spf:
        sumBottomNode[key] = mode_spf[key] + nodes_spf[key]
    BottomSum = sum([l_[1] for l_ in sumBottomNode.items()])

    for i in range(maxNodes):
        if basis.MCTDHnode(i).Toplayer() == True:
                children = basis.MCTDHnode(i).NChildren()
                for j in range(children):
                    SumTopNode += basis.MCTDHnode(i).down(j).t_dim().GetnTensor()
                SumTopNode += basis.MCTDHnode(i).t_dim().GetnTensor()

    for i in range(maxNodes):
        if basis.MCTDHnode(i).Toplayer() == False and basis.MCTDHnode(i).Bottomlayer() == False:
                children = basis.MCTDHnode(i).NChildren()
                parent = basis.MCTDHnode(i).t_dim().GetnTensor()
                for j in range(children):
                    remnantNode += basis.MCTDHnode(i).down(j).t_dim().GetnTensor() 
                    
                remnantNode += parent
                remnantNodeList.append(remnantNode)
                remnantNode = 0
    remnantSum = sum(remnantNodeList)

    return BottomSum + SumTopNode + remnantSum

print get_SPFs()