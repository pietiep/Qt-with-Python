class Tree():
    def __init__(self, startSPF):
        self._rootNode0 = LightNode("TOP")
        self._rootNode = LightNode(str(startSPF), self._rootNode0)
        self._dictNodes = {}

    def addNode(self, obj, SPF, parent):
        self._dictNodes[obj] = Node(SPF, parent)


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

#    @classmethod
#    def initFromList(cls, nodeList):
#        objList = []
#        for node in nodeList:


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

 #   dict_nodes = {}
 #   rootNode0 = LightNode("TOP")
 #   rootNode = LightNode("36", rootNode0)
#    node2 = Node("30", rootNode)
#    node1 = Node("19", rootNode)
#    node3 = Node("9", node1)
#    childNode0 = LightNode("19", rootNode)
#    childNode1 = Node("30", rootNode)
#    childNode2 = Node("9", childNode0)
#    childNode3 = Node("4", childNode0)
#    childNode4 = Node("17", childNode1)
#    childNode5 = Node("17", childNode1)
#    childNode6 = BottomNode("24", childNode2, "3")

    tree = Tree("36")
    tree.addNode("child0", "19", tree._rootNode)
    tree.addNode("child2", "9", tree._dictNodes["child0"])

 #   def addNode(obj, SPF, parent):
 #       dict_nodes[obj] = Node(SPF, parent)
 #       return dict_nodes
#
 #   dict_nodes = addNode("childNode0", "19", rootNode)
 #   dict_nodes = addNode("childNode2", "9",  dict_nodes["childNode0"])

    print tree._rootNode
