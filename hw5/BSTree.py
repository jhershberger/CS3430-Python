from BSTNode import BSTNode

## bugs to vladimir dot kulyukin at usu dot edu

class BSTree:

    def __init__(self, root=None):
        self.__root = root
        if root==None:
            self.__numNodes = 0
        else:
            self.__numNodes = 1

    def getRoot(self):
        return self.__root

    def getNumNodes(self):
        return self.__numNodes

    def isEmpty(self):
        return self.__root == None

    ## implement this method
    def hasKey(self, key):
        d = {}
        currNode = self.__root

        while currNode != None:
            if currNode.getKey() == key:
                return True
            elif key < currNode.getKey():
                currNode = currNode.getLeftChild();
            else:
                currNode = currNode.getRightChild();

        return False

    def insertKey(self, key):
        if self.isEmpty():
            self.__root = BSTNode(key=key)
            self.__numNodes += 1
            return True
        elif self.hasKey(key):
            return False
        else:
            currNode = self.__root
            parNode = None
            while currNode != None:
                parNode = currNode
                if key < currNode.getKey():
                    currNode = currNode.getLeftChild()
                elif key > currNode.getKey():
                    currNode = currNode.getRightChild()
                else:
                    raise Exception('insertKey: ' + str(key))
            if parNode != None:
                if key < parNode.getKey():
                    parNode.setLeftChild(BSTNode(key=key))
                    self.__numNodes += 1
                    return True
                elif key > parNode.getKey():
                    parNode.setRightChild(BSTNode(key=key))
                    self.__numNodes += 1
                    return True
                else:
                    raise Exception('insertKey: ' + str(key))
            else:
                raise Exception('insertKey: parNode=None; key= ' + str(key))

    ## implement this method
    def __heightOf(self, node):
        if node is None:
            return -1
        else:
            #print 'max = ', 1 + max(self.__heightOf(node.getLeftChild()), self.__heightOf(node.getRightChild()))
            return 1 + max(self.__heightOf(node.getLeftChild()), self.__heightOf(node.getRightChild()))

    def heightOf(self):
        return self.__heightOf(self.__root)

    ## implement this method
    def isBalanced(self):
        height_right = self.__heightOf(self.__root.getRightChild())
        height_left = self.__heightOf(self.__root.getLeftChild())
        if abs(height_left - height_right) <= 1:
            return True
        else:
            return False

    def __displayInOrder(self, currnode):
        if currnode == None:
            print('NULL')
        else:
            self.__displayInOrder(currnode.getLeftChild())
            print(str(currnode))
            self.__displayInOrder(currnode.getRightChild())

    def displayInOrder(self):
        self.__displayInOrder(self.__root)

    ## implement this method
    def isList(self):
        # a bst is linear if the num nodes is exactly one greater than the height
        height_plus_one = self.heightOf() + 1
        num_nodes = self.getNumNodes()
        if num_nodes == height_plus_one:
            return True
        else:
            return False;
