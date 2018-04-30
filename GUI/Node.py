from LogicalNodes import LogicalNodes
from ModelTree import ModelTree
import networkx as nx
import re

class Parameters(object):
    def __init__(self):
        self._eps_general =  None
        self._eps_1 = None
        self._eps_2 = None
        self._start = None
        self._end = None
        self._dt = None
        self._iteration = None
        self._hamiltonian = None
        self._potential = None
        self._job = None
        self._parameters = None
        self._treeData = None

class InPut(Parameters):
    def __init__(self, filename='example.in'):
        super(InPut, self).__init__()
        self._filename = filename
        self._paradict = {}
        self._paralist = []
        self.readFile()

    def readFile(self):
        self.getPara("eps_general")
        self.getPara("eps_1")
        self.getPara("eps_2")
        self.getPara("start")
        self.getPara("end")
        self.getPara("dt")
        self.getPara("iteration")
        self.getPara("Hamiltonian")
        self.getPara("Potential")
        self.getPara("job")
        self.getPara2()
        self._paradict['para'] = self._paralist
        print self._paradict['start']
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'
        print 'helo'


    def getPara2(self):
        with open(self._filename, "rb") as text:
            for line in text:
                if "parameters" in line:
                    for i in range(10):
                        try:
                            para = text.next()
                            if bool(re.search(r'\d', para)):
                                para = para.split()     #if para contains numbers
                                self._paralist.append(para)
                        except StopIteration:
                            pass
#                    while bool(re.search(r'\d', line)):

    def getPara(self, para):
        with open(self._filename, "rb") as text:
            for line in text:
                if para in line:
                    pos = line.index('=')     # get Index
                    self._paradict[para] = line[pos+1:].strip()  # removes whitestripes

class OutPut(Parameters):
    def __init__(self, tree, paradict, sysFile, filename="example.in"):
        print paradict['job']
        self._eps_general = paradict['eps_general']
        self._eps_1 = paradict['eps_1']
        self._eps_2 = paradict['eps_2']
        self._start = paradict['start']
        self._end =paradict['end']
        self._dt = paradict['dt']
        self._iteration = paradict['iteration']
        self._hamiltonian = paradict['Hamiltonian']
        self._potential = paradict['Potential']
        self._job = paradict['job']
        self._parameters = paradict['para']
        self._formated = self.formatparameter()
        self._treeData = tree._treeData
        self._filename = filename
        self._sysFile = sysFile
        print filename, sysFile
#        self.savefile()
#        self.savefile2()

    def savefile(self):
        with open(self._filename, "w") as text_file:
            text_file.write("{0}".format(self.bringAllTogether()))

    def savefile2(self):
        with open(self._sysFile, "w") as text_file:
            text_file.write("{0}".format(self.bringTreePara()))

    def formatparameter(self):
        output = ""
        for row_ in self._parameters:
                for ele_ in row_:
                    if row_[-1] == ele_:
                        output += str(ele_) + "\n"
                    else:
                        output += str(ele_) + "  "
        return output

    def bringAllTogether(self):
        output = "eps = { \n" \
        "eps_general = " + self._eps_general + "\n" \
        "eps_1 =" + self._eps_1 + "\n" \
        "eps_2 =" + self._eps_2 + "\n" \
        "} \n" \
        "\n" \
        "integrator = { \n" \
        "start = " + self._start + "\n" \
        "end = " + self._end + "\n" \
        "dt = " + self._dt + "\n" \
        "iteration = " + self._iteration + "\n" \
        "} \n" \
        "\n" \
        "Hamiltonian = " + self._hamiltonian + "\n" \
        "Potential = " + self._potential + "\n" \
        "\n" \
        "job = " + self._job + "\n" \
        "\n" \
        "\n" \
        "basis = \n" \
        "{\n" \
        "tree = [ \n" \
         + self._treeData + \
        "]\n" \
        "\n" \
        "\n" \
        "parameters = [\n" \
        + self._formated + \
        "]\n" \
        "}"
        return output

    def bringTreePara(self):
        output =  self._treeData + \
        "\n" \
        + self._formated
        return output

    def __repr__(self):
        return self.bringAllTogether()


class Tree(object):
#    def __init__(self):
    def __init__(self, mctdhConfig, sys_file):
        self._rootNode0 = Node("TOP")
        self._dictNodes = {}

        print mctdhConfig, 'from Tree'
        print sys_file, 'from Tree'

        model = ModelTree(mctdhConfig, sys_file)
        logical = LogicalNodes(model.lay_matr_mode, mctdhConfig, sys_file)
        self._G = logical.G
        self._elder = None
        self.getElder()
        self.addNode(self._elder, str(self._G.nodes[self._elder]['SPF']), self._rootNode0)
        self.readTree()

        self._rootNode = self._dictNodes[10]
        self._treeData = self._dictNodes[10].log()

    def getElder(self):
        for ele_ in self._G.nodes():
            if self._G.pred[ele_] == {}:
                self._elder = ele_
        self._elder = self._G.successors(self._elder).next()


    def readTree(self):
        for suc_ in nx.bfs_successors(self._G, self._elder):
            for brothers in suc_[1]:
                if 'Mode' in self._G.nodes[brothers].keys():
                    self.addBottomNode(brothers, str(self._G.nodes[brothers]['SPF']), self._dictNodes[suc_[0]], str(self._G.nodes[brothers]['Mode']))
                else:
                    self.addNode(brothers, str(self._G.nodes[brothers]['SPF']), self._dictNodes[suc_[0]]) #Label, SPF, parent_obj

    def setRootNode(self, rootNode):
        self._rootNode = rootNode
        self.setLog()

    def setLog(self):
        self._treeData = self._rootNode.log()

    def addNode(self, obj, SPF, parent):
        self._dictNodes[obj] = Node(SPF, parent)

    def addBottomNode(self, obj, SPF, parent, physcoor):
        self._dictNodes[obj] = BottomNode(SPF, parent, physcoor)

class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False

        try:
            child = self._children.pop(position)
            child._parent = None
            return True
        except IndexError as e:
            print e.message, ': from Node, 237'
            return False

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def childcount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "   "
        if self.childcount() == 0:
            output += self._name + "  " + str(self.childcount()) + "\n"
        else:
            output += self._name + " -" + str(self.childcount()) + "\n"

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1
#        output += "\n"

        return output

    def __repr__(self):
        return self.log()

    def typeInfo(self):
        return "NODE"

class TransformNode(Node):
    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)

    def typeInfo(self):
        return "Transform"

class CameraNode(Node):
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)

    def typeInfo(self):
        return "CAMERA"

class LightNode(Node):
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)

    def typeInfo(self):
        return "LIGHT"

class BottomNode(Node):
    def __init__(self, name, parent, physcoor):
        super(BottomNode, self).__init__(name, parent)
        self._physcoor = physcoor

    def typeInfo(self):
        return "Bottom"

    def setPhyscoor(self, physcoor):
        self._physcoor = physcoor

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "   "
        if self.childcount() == 0:
            output += self._name + "  " + str(self.childcount()) + "   " + self._physcoor + "\n"
        else:
            output += self._name + " -" + str(self.childcount()) + "\n"

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1
#        output += "\n"

        return output

if __name__ == '__main__':

    tree = Tree("36")
    inobj = InPut()