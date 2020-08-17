
# convention: [(+,+), (+,-), (-,-), (+,+)]

import random

#bounds: ((x,y), radius)
class QuadTreeNode:
    def __init__(self, bounds, parent = None):
        self.parent = parent
        self.nodes = []
        self.bounds = bounds
        
    def toList(self):
        out = []
        for n in self.nodes:
            if type(n) is QuadTreeNode:
                out += n.toList()
            elif type(n) is Element:
                out.append(n)
        return out
    
    def __str__(self):
        if len(self.nodes) == 0:
            return "[None]"
        else:
            return f"[{self.nodes[0]}, {self.nodes[1]}, {self.nodes[2]}, {self.nodes[3]}]"
        return str(self.nodes)
    
    def insert(self, element):
        if len(self.nodes) == 0:
            self.nodes = [None, None, None, None]
            i = self.bounds.where(element)
            self.nodes[i] = element
        else:
            i = self.bounds.where(element)
            if self.nodes[i] is None:
                self.nodes[i] = element
            else:
                if type(self.nodes[i]) is QuadTreeNode:
                    self.nodes[i].insert(element) # insert into existing node
                elif type(self.nodes[i]) is Element:
                    if element.x == self.nodes[i].x and element.y == self.nodes[i].y:
                        raise Exception(f"Collision between new element {element} and existing element {self.nodes[i]}")
                    #make a new QuadTreeNode
                    newbounds = self.bounds.newbounds(i)
                    newnode = QuadTreeNode(newbounds, self)
                    # put the existing element in it
                    newnode.insert(self.nodes[i])
                    # put the new element in it
                    newnode.insert(element)
                    # store the new node as a child
                    self.nodes[i] = newnode
                else:
                    raise Exception(f"Can't insert into type {type(self.nodes[i])}!")
                    
                
    def size(self):
        if len(self.nodes == 0):
            return None
        else:
            return sum(x is not None for x in self.nodes)            
            
    
    def contains(self, element : 'Element'):
        return False
    
    def remove(self, element):
        return
        
    def find_closest(self, element):
        return
        
class Bounds:
    def __init__(self, x_start, x_end, y_start, y_end):
        if x_start > x_end:
            raise Exception("X Coords reversed!")
        if y_start > y_end:
            raise Exception("Y Coords reversed!")
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.center = ((x_start+x_end)/2, (y_start+y_end)/2)

    def __str__(self):
        return f"({self.x_start}-{self.x_end}, {self.y_start}-{self.y_end})"
        
    def newbounds(self, i):
        if i == 0:
            return Bounds(self.center[0], self.x_end, self.center[1], self.y_end)
        if i == 1:
            return Bounds(self.center[0], self.x_end, self.y_start, self.center[1])
        if i == 2:
            return Bounds(self.x_start, self.center[0], self.center[1], self.y_end)
        if i == 3:
            return Bounds(self.x_start, self.center[0], self.y_start, self.center[1])
        raise Exception("Quad index out of bounds!")
        
    def where(self, elem: 'Element'):
        """Returns the index of the quadrant where elem belongs"""
        if elem.x < self.x_start or elem.x > self.x_end \
            or elem.y < self.y_start or elem.y > self.y_end:
                raise Exception("Value out of bounds!")
        out = 0
        if elem.x < self.center[0]:
            out += 2
        if elem.y < self.center[1]:
            out += 1
        return out
    
class Element:
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v
        
    def __str__(self):
        return f"({self.x}, {self.y}) {self.v}"
    def __repr__(self):
        return str(self)
    
    def generate(bounds : Bounds):
        return Element(random.randint(bounds.x_start, bounds.x_end),
                       random.randint(bounds.y_start, bounds.y_end), random.randint(0, 100))
            
if __name__ == "__main__":
    b = Bounds(-100, 100, -100, 100)
    tree = QuadTreeNode(b, None)
    for i in range(10):
        tree.insert(Element.generate(b))
    print(tree)