class Node:
    def __init__(self):
        self.l = None
        self.r = None
        self.v = 0
    
    def add(self):
        self.v += 1

class Tree:
    def __init__(self):
        self.root = Node()
        
    def add_num(self, num):
        self.root.add()
        self._add_num(num, self.root)
        
    def _add_num(self, num, node):
        if len(num) > 0:
            if node.l is None: 
                node.l = Node()
                node.r = Node()
                
            if num[0] == '0': node = node.l
            else: node = node.r
                    
            node.add()
            self._add_num(num[1:], node)
            
    def traverse_more(self):
        out = ''
        node = self.root
        while node.r is not None:
            if node.r.v >= node.l.v:
                out += '1'
                node = node.r
            else:
                out += '0'
                node = node.l
                
        return int(out, 2)
    
    def traverse_less(self):
        out = ''
        node = self.root
        while node.r is not None:
            if (node.r.v < node.l.v and node.r.v > 0) or node.l.v == 0:
                out += '1'
                node = node.r
            else:
                out += '0'
                node = node.l
                
        return int(out, 2)
              
if __name__ == '__main__':
    data_path = "data/input03"
    bin_tree = Tree()

    # Read line-by-line
    f = open(data_path, "r")
    for x in f:
        bin_tree.add_num(x.strip())

    print(f'Support rating {bin_tree.traverse_more() * bin_tree.traverse_less()}')