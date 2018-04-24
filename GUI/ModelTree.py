import mctdh
import sys

class ModelTree(object):
    def __init__(self, config_file='mctdh.config', sys_file='CH3g1.txt'):
        self.config_file = config_file
        self.sys_file = sys_file
        self.bottom_list = []
        self.mode_list =[]
        self.layer_list = []
        self.layer_matr = []
        self.lay_matr_mode = []
        self.label_mode = {}
        self.nodes_spf = {}

        print self.config_file, 'from ModelTree'
        print self.sys_file, 'from ModelTree'
        self.config = mctdh.controlParameters()
        self.config.initialize(self.config_file)
        self.basis = mctdh.MctdhBasis()
        self.basis.initialize(self.sys_file, self.config)
        self.node = mctdh.MctdhNode()
        self.phys = mctdh.PhysCoor()
        self.tdim = mctdh.Tdim()

        self.getLayerMatr()
        self.getPhysCoord()
        self.modeToGetLayer()
        self.get_SPFs()


    def getBottomlayer(self):
        """Get the bottom nodes"""
        for i in range(self.basis.NmctdhNodes()):
            self.node = self.basis.MCTDHnode(i)
            if self.node.Bottomlayer() == True:
                self.bottom_list.append(i)
        return self.bottom_list #List of the i-th bottom node

    def getPhysCoord(self):
        """get the Modes of the pys. Coordinates"""
        for i in range(self.basis.NmctdhNodes()):
            self.node = self.basis.MCTDHnode(i)
            if self.node.Bottomlayer() == True:
                self.phys = self.node.phys_coor()
                self.mode_list.append(self.phys.mode()) #append Modes to list

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
        self.layer_matr = [list(reversed(self.nlayer(b_))) for b_ in self.getBottomlayer()]

    def modeToGetLayer(self):
        """Combines layer_matr with mode_list"""
        self.lay_matr_mode = [l_ + [100 + i] for i,l_ in enumerate(self.layer_matr)]
        self.lay_matr_mode = [["Top"] + l_ for l_ in self.lay_matr_mode]
        #concatinates two lists
        self.label_mode = [100 + i for i in range(len(self.mode_list))]
        self.label_mode = dict(zip(self.label_mode, self.mode_list))

    def get_SPFs(self):
        """get the SPFs of each Node"""
        for i in range(self.basis.NmctdhNodes()):
            self.node = self.basis.MCTDHnode(i)
            self.tdim = self.node.t_dim()
            self.nodes_spf[i] = self.tdim.GetnTensor() #dict

        mode_spf = [self.basis.MCTDHnode(i).t_dim().active(0) for i in \
                    range(self.basis.NmctdhNodes()) if \
                    self.basis.MCTDHnode(i).Bottomlayer() == True ]

        mode_spf_dict = dict(zip(self.label_mode, mode_spf))
        for k, i in zip(self.label_mode.keys(), mode_spf):
            self.nodes_spf[k] = i



if __name__ == '__main__':

    model = ModelTree()
#    model.getLayerMatr()
#    model.getPhysCoord()
#    model.modeToGetLayer()
    print model.mode_list
    print model.layer_matr
    print model.lay_matr_mode
    print model.label_mode
    print model.nodes_spf
