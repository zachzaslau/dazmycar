# B+ Tree implementation in Python
# Start with first node, insert into key (price) and value (car) until it overflows (key>order-1)
# After overflow split the nodes into two nodes based on index order/2, split the keys and values into two nodes
# Then copy the middle key to a new parent node which will now be the root node, no values, but now has two children, the two nodes that were split (based on left, less than, and right, greater than)
# To insert next, now you traverse down to a leaf node using the internal nodes as 'sign' posts. Compare the key to the keys in the internal node, and traverse down to the left (k<key) or right child (k>=key) based on comparison.
# Once you reach a leaf node, insert the key and value into that leaf node.
# If it overflows, split the leaf node and copy the middle key to the parent internal node. If the parent internal node overflows, repeat the process of splitting and copying up to the root. If the root overflows, create a new root with two children.


class Node ():
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []  # Only used for internal nodes to store child pointers
        self.values = []  # Only used for leaf nodes: values[i] is a LIST of cars whose price is keys[i]
        self.next = None  # Pointer to the next leaf node (used for leaf nodes)
        self.parent = None


class BPlusTree ():
    def __init__(self, order=4):
        self.root = Node(is_leaf=True)
        self.order = order

    def find_leaf(self, price):
        current_node = self.root
        while(not current_node.is_leaf):
            temp = current_node.keys
            for i in range(len(temp)):
                if(price < temp[i]):
                    current_node = current_node.children[i]
                    break
            else:
                current_node = current_node.children[len(temp)]
        return current_node

    def search_min(self, price):
        current_node = self.find_leaf(price)
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
                    carList.extend(current_node.values[i])
                if(current_node.keys[i] > maxPrice):
                    return carList
            current_node = current_node.next

        return carList

    def split(self, node):
        mid = len(node.keys)//2
        if(node.is_leaf):
            new_node = Node(True)
            new_node.keys = node.keys[mid:]
            new_node.values = node.values[mid:]
            up_key = new_node.keys[0]
            del node.keys[mid:]
            del node.values[mid:]
            new_node.next = node.next
            node.next = new_node
        else:
            new_node = Node()
            up_key = node.keys[mid]
            new_node.keys = node.keys[mid+1:]
            new_node.children = node.children[mid+1:]
            del node.keys[mid:]
            del node.children[mid+1:]
            for i in range(len(new_node.children)):
                new_node.children[i].parent = new_node

        if(node.parent != None):
            new_node.parent = node.parent
            for i in range(len(node.parent.keys)):
                if(node.parent.keys[i] >= up_key):
                    node.parent.keys.insert(i, up_key)
                    node.parent.children.insert(i+1, new_node)
                    break
            else:
                node.parent.keys.append(up_key)
                node.parent.children.append(new_node)
            if(len(node.parent.keys) > (self.order) - 1):
                self.split(node.parent)
        else:
            new_root = Node()
            new_root.keys.append(up_key)
            new_root.children = [node, new_node]
            node.parent = new_root
            new_node.parent = new_root
            self.root = new_root

    def insert(self, car):
        node = self.find_leaf(car.price)
        for i in range(len(node.keys)):
            if(node.keys[i] == car.price):
                node.values[i].append(car)
                return
            if(node.keys[i] > car.price):
                node.keys.insert(i, car.price)
                node.values.insert(i, [car])
                break
        else:
            node.keys.append(car.price)
            node.values.append([car])
        if(len(node.keys) > (self.order)-1):
            self.split(node)