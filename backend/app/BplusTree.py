# B+ Tree implementation in Python
# Start with first node, insert into key (price) and value (car) until it overflows (key>order-1)
# After overflow split the nodes into two nodes based on index order/2, split the keys and values into two nodes
# Then copy the middle key to a new parent node which will now be the root node, no values, but now has two children, the two nodes that were split (based on left, less than, and right, greater than)
# To insert next, now you traverse down to a leaf node using the internal nodes as 'sign' posts. Compare the key to the keys in the internal node, and traverse down to the left (k<key) or right child (k>=key) based on comparison. Once you reach a leaf node, insert the key and value into that leaf node. 
# If it overflows, split the leaf node and copy the middle key to the parent internal node. If the parent internal node overflows, repeat the process of splitting and copying up to the root. If the root overflows, create a new root with two children.

class Node ():
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = [] #Only used for internal nodes to store child pointers
        self.values = []  # Only used for leaf nodes to store values associated with keys
        self.next = None  # Pointer to the next leaf node (used for leaf nodes)
    

class BPlusTree ():
      root = None
      order = 4  # Default order of the B+ tree
      def __init__(self, order=4):
        self.root = Node(is_leaf=True)
        self.order = order
    

