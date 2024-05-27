# Harinderjit Malhi
# node.py

class Node:
    def __init__(self, x, y, is_wall=False, parent = None, cost = float('inf')):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.parent = parent
        self.neighbors = []
        self.cost = cost
        self.explored = False  # Add this attribute


    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def is_passable(self):
        return not self.is_wall
    