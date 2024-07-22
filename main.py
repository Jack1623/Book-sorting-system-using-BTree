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

            if len(node.values)>4:
                left_node = BTreeNode()
                right_node = BTreeNode()
                left_node.values = node.values[:2]
                right_node.values = node.values[3:]
                node.values = [node.values[2]]
                node.children = [left_node, right_node]

def print_tree(node, level=0):
    if node is not None:
        print(f"Level {level}: {node.values}")
        for child in node.children:
            print_tree(child, level+1)

btree = BTree()
values_insert = [1, 2, 3, 4, 5, 6, 7, 8]
for value in values_insert:
    btree.insert(value)

print_tree(btree.root)