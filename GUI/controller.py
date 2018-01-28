from ModelTree import ModelTree
from view import View


class Controller(object):
    def __init__(self):
        self.model = ModelTree()
        self.putout()

    def putout(self):
        print self.model.getBottomlayer()
        self.model.getLayerMatr()
#        print self.model.nlayer

C = Controller()
