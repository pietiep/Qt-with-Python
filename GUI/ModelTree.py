import mctdh

class ModelTree(object):
    def __init__(self, config_file='mctdh.config', sys_file='CH3g1.txt'):
        self.config_file = config_file
        self.sys_file = sys_file
        self.bottom_list = []
        self.layer_list = []
        self.config = mctdh.controlParameters()
        self.config.initialize(self.config_file)
        self.basis = mctdh.MctdhBasis()
        self.basis.initialize(self.sys_file, self.config)
        self.node = mctdh.MctdhNode()
    def getBottomlayer(self):
        """Get the bottom nodes"""
        for i in range(self.basis.NmctdhNodes()):
            self.node = self.basis.MCTDHnode(i)
            if self.node.Bottomlayer() == True:
                self.bottom_list.append(i)
        return self.bottom_list #List of the i-th bottom node
    def nlayer(self, i):
        """Recursion function that goes from the i-th node up to the top layer of the tree"""
        self.node = self.basis.MCTDHnode(i) #i-th Node
        self.layer_list.append(i)
        if self.node.Toplayer() == False:
            return self.nlayer(self.node.up().address())
        new_list = list(self.layer_list) #copy instead of reference
        del self.layer_list[:]
        return new_list
    def getLayerMatr(self):
        """Takes all bottom nodes and returns for each a list of the path to the top node"""
        return [list(reversed(self.nlayer(b_))) for b_ in self.getBottomlayer()]
