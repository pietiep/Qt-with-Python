class OutPut(object):
    def __init__(self, eps, integrator, hamiltonian, potential, \
                 job, parameters, tree, filename="example.in"):
        self._eps_general = eps[0]
        self._eps_1 = eps[1]
        self._eps_2 = eps[2]
        self._start = integrator[0]
        self._end =integrator[1]
        self._dt = integrator[2]
        self._iteration = integrator[3]
        self._hamiltonian = hamiltonian
        self._potential = potential
        self._job = job
        self._parameters = parameters
        self._formated = self.formatparameter()
        self._treeData = tree._treeData
        self.savefile(filename)
        self.savefile2()

    def savefile(self, filename):
        with open(filename, "w") as text_file:
            text_file.write("{0}".format(self.bringAllTogether()))

    def savefile2(self):
        with open("CH3g1.txt", "w") as text_file:
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
    def __init__(self, startSPF):
        self._rootNode0 = Node("TOP")
        self._rootNode = Node(str(startSPF), self._rootNode0)
        self._childNode0 = Node("19", self._rootNode)
        self._childNode1 = Node("30", self._rootNode)
        self._childNode2 = Node("9", self._childNode0)
        self._childNode3 = Node("4", self._childNode0)
        self._childNode4 = Node("17", self._childNode1)
        self._childNode5 = Node("17", self._childNode1)
        self._childNode6 = BottomNode("24", self._childNode2, "3")
        self._childNode7 = BottomNode("12", self._childNode3, "0")
        self._childNode8 = Node("5", self._childNode4)
        self._childNode9 = Node("7", self._childNode4)
        self._childNode10 = Node("5", self._childNode5)
        self._childNode11 = Node("7", self._childNode5)
        self._childNode13 = BottomNode("12", self._childNode8, "1")
        self._childNode12 = BottomNode("12", self._childNode9, "4")
        self._childNode14 = BottomNode("12", self._childNode10, "2")
        self._childNode15 = BottomNode("12", self._childNode11, "5")
        self._treeData = self._rootNode.log()
        self._dictNodes = {}

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

        self._children.pop(position)
        child._parent = None
        return True

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

#    tree = Tree("36")

 #   dict_nodes = addNode("childNode0", "19", rootNode)
 #   dict_nodes = addNode("childNode2", "9",  dict_nodes["childNode0"])
#    print tree._rootNode

#    output = tree._rootNode.log()
#    print output

    eps = ["1E-5", "1E-6", "1E-5"]
    integrator = ["0", "1000", "0.1", "100"]
    hamiltonian = "194"
    potential = "101"
    job = "eigenstates"
    parameters = [[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16],
                  [17, 18, 19, 20],
                  [21, 22, 23, 24]]

    filedata = OutPut(eps, integrator, hamiltonian, potential, job, parameters, tree)
    print filedata
#    with open("example.in", "w") as text_file:
#        text_file.write("{0}".format(filedata))
