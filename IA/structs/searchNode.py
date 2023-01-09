"""
    parent: is the parent node.
    state: is the state of the node.
    f: is the estimated cost.
    g: is the cost from the initial node to the current node.
    h: is the cost from the current node to the nearest target.
"""
class Node:
    def _init_(self, parent, state, f, g, h):
        self.parent = parent
        self.state = state
        self.f = f
        self.g = g
        self.h = h
    