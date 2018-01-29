from ModelTree import ModelTree
from LogicalNodes import LogicalNodes
from view import View


class Controller(object):
    def __init__(self):
        self.model = ModelTree()
        self.model2 = LogicalNodes()
        self.berechne()

    def berechne(self):
        pass
        #processing
        self.model.getLayerMatr()
        self.model2.Networkx(self.model.layer_matr)
    #    self.model.getLayerMatr()
    #    return self.model.layer_matr
        #output

C = Controller()
