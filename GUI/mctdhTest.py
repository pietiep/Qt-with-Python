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

def get_SPFs():
    """get the SPFs of each Node"""
    for i in range(maxNodes):
        node = basis.MCTDHnode(i)
        tdim = node.t_dim()
        nodes_spf[i] = tdim.GetnTensor() #dict

    mode_spf = {i: basis.MCTDHnode(i).t_dim().active(0) for i in \
                range(maxNodes) if \
                basis.MCTDHnode(i).Bottomlayer() == True}
                
    for key in mode_spf:
        sumBottomNode[key] = mode_spf[key] + nodes_spf[key]



    SumTopNode = 0
    for i in range(maxNodes):
        if basis.MCTDHnode(i).Toplayer() == True:
                children = basis.MCTDHnode(i).NChildren()
                for j in range(children):
                    SumTopNode += basis.MCTDHnode(i).down(j).t_dim().GetnTensor()

    remnantNode = 0
    remnantNodeDict = {}
    for i in range(maxNodes):
        if basis.MCTDHnode(i).Toplayer() == False and basis.MCTDHnode(i).Bottomlayer() == False:
                children = basis.MCTDHnode(i).NChildren()
                parent = basis.MCTDHnode(i).t_dim().GetnTensor()
                for j in range(children):
                    remnantNode += basis.MCTDHnode(i).down(j).t_dim().GetnTensor() 
                    
                remnantNode += parent
                remnantNodeDict[i] = remnantNode
                remnantNode = 0
    print remnantNodeDict + SumTopNode + sumBottomNode

    def sumOfDicts(*dict_arg):
        for dicts in *dict_args:
            print dicts

#    for i in range()

get_SPFs()