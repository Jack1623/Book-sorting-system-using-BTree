class BTreeNode:
    def __init__(self):
        self.values = []
        self.children = []

class BTree:
    def __init__(self):
        self.root = BTreeNode()

    def insert(self, value):
        self.insert_value(self.root, value)

def insert_value(self, node, value):
    if not node.children:
        node.values.append(value)
        node.values.sort()

        if len(node.values>4):
            left_node = BTreeNode()
            right_node = BTreeNode()
            left_node.values = node.values[:2]
            right_node.values = node.values[3:]
            node.values = [node.values[2]]
            node.children = [left_node, right_node]