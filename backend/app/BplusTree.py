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
        self.parent = None
    

class BPlusTree ():
    root = None
    order = 4  # Default order of the B+ tree
    def __init__(self, order=4):
        self.root = Node(is_leaf=True)
        self.order = order

    def search_min(self, price):
        current_node = self.root
        while(not current_node.is_leaf):
            temp = current_node.keys
            for i in range(len(temp)):
                if(price < temp[i]):
                    current_node = current_node.children[i]
                    break
            else:
                current_node = current_node.children[len(temp)]

        for i in range(len(current_node.keys)):
            if(current_node.keys[i] >= price):
                return current_node
        else:
            return current_node.next

    def search_range(self, node, minPrice, maxPrice):
        carList = []
        current_node = node
        while(current_node != None):
            for i in range(len(current_node.keys)):
                if(current_node.keys[i] >= minPrice and current_node.keys[i] <= maxPrice):
                    carList.append(current_node.values[i])
                if(current_node.keys[i] > maxPrice):
                    break
            current_node = current_node.next

        return carList

    def split(self, node):
        mid = len(node.keys)//2
        if(node.is_leaf):
            temp = Node(True)
            temp.keys = node.keys[mid:]
            temp.values = node.values[mid:]
            del node.keys[mid:]
            del node.values[mid:]
            temp.parent = node.parent
            temp.next = node.next
            node.next = temp
        else:
            temp2 = Node()
            temp2.keys = node.keys[mid+1:]
            temp2.children = node.children[mid+1:]
            del node.keys[mid:len(node.keys)]
            del node.children[mid+1:]
            temp2.parent = node.parent
            for i in range(len(temp2.children)):
                temp2.children[i].parent = temp2      
        if(node.parent != None):
            for i in range(len(node.parent.keys)):
                if(node.parent.keys[i] >= node.keys[mid]):
                    node.parent.keys.insert(i, node.keys[mid])
                    break
            if(len(node.parent.keys) > (self.order) -1):
                self.split(node.parent)
        else:
            node.parent = Node()
            self.root = node.parent
            node.parent.keys.append(node.keys[mid])
        

    def insert(self, car):
        node = self.search_min(car.price())
        for i in range(len(node.keys)):
            if(node.keys[i] >= car.price()):
                node.keys.insert(i, car.price())
                node.values.insert(i, car)
                break
        if(len(node.keys) > (self.order)-1):
            self.split(node)

#HELLO

# Start with first node, insert into key (price) and value (car) until it overflows (key>order-1)
# After overflow split the nodes into two nodes based on index order/2, split the keys and values into two nodes
# Then copy the middle key to a new parent node which will now be the root node, no values, but now has two children, the two nodes that were split (based on left, less than, and right, greater than)
# To insert next, now you traverse down to a leaf node using the internal nodes as 'sign' posts. Compare the key to the keys in the internal node, and traverse down to the left (k<key) or right child (k>=key) based on comparison. Once you reach a leaf node, insert the key and value into that leaf node. 
# If it overflows, split the leaf node and copy the middle key to the parent internal node. If the parent internal node overflows, repeat the process of splitting and copying up to the root. If the root overflows, create a new root with two children.