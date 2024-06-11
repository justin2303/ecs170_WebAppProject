import time
from flask import request, jsonify
from api import app

@app.route("/api/algorithm/astar", methods=["POST"])
def solve_maze_astar():
    maze = request.json.get('maze')
    start_coords = tuple(request.json.get('start_coords'))
    end_coords = tuple(request.json.get('end_coords'))
    
    try:
        start_time = time.perf_counter()
        solution = astar(maze, start_coords, end_coords)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        if not solution:
            raise Exception("No path")
    except Exception as e:
        print(e)
        return jsonify( {'error': str(e)} ), 400
    
    return jsonify({ 'solution': solution, 'timeElapsed': elapsed_time }), 200


# Katie Sharp
import heapq

class Node:

    def __init__(self, parent = None, position = None):
        
        self.parent = parent
        self.position = position
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0

    # make sure that the heapq will sort nodes in terms of f cost
    def __lt__(self, other):
      return self.fcost < other.fcost
    
    def __gt__(self, other):
      return self.fcost > other.fcost

# function to return the solution to the maze as a list of ordered pairs
def return_path(current_node):
    path = []
    curr_node = current_node
    
    while curr_node is not None:
        path.append(curr_node.position)
        curr_node = curr_node.parent
    
    return path[::-1]  # Return reversed path

# astar function that solves the maze
def astar(maze, start, end):  
    
    # Create start and end nodes
    start_node = Node(None, start)
    start_node.gcost = 0
    start_node.hcost = 0
    start_node.fcost = 0

    end_node = Node(None, end)
    end_node.gcost = 0
    end_node.hcost = 0
    end_node.fcost = 0

    # Initialize both open and closed list
    open_spots = [] # nodes that have been discovered but not yet evaluated
    closed_spots = [] # nodes that have been discovered AND evaluated

    # Heapify the open_list and Add the start node
    heapq.heapify(open_spots)
    heapq.heappush(open_spots, start_node)

    # orthogonal spots to search
    spots_search = ((0,1),(0,-1),(1,0),(-1,0))

    while (len(open_spots) > 0):
        
        #pop the node from the openlist and set it as current node
        current_node = heapq.heappop(open_spots)
        
        #then append the current node to the closed nodes list 
        closed_spots.append(current_node)

        # check if the current node is the end node, if it is, return the path
        if current_node.position == end_node.position:
            return return_path(current_node)

        # Initialize list of children aka possible next spots for the current node to go to
        children = []

        # transform spots_search into nodes of orthogonal children for current node and populate the children list
        for new_spot in spots_search:
            node_spot = (current_node.position[0] + new_spot[0], current_node.position[1] + new_spot[1])

            # make sure that the new node is in the scope of the maze
            if (node_spot[0] >= len(maze)) or (node_spot[0] < 0) or (node_spot[1] >= len(maze[0])) or (node_spot[1] < 0):
                continue # this means, if any of those above conditions are true, go to the next new_spot in the spots_search

            # make sure that the node_spot is traversable (not a wall in the maze)
            if maze[node_spot[0]][node_spot[1]] != 0:
                continue 
            
            # make sure that the node_spot is not in the closed list 
            isInClose = False
            for check_node in closed_spots:
                if node_spot == check_node.position:
                    isInClose = True

            if isInClose == True:
                continue
            
            # once all checks pass, initiialize a new node for the orthogonal spot and add it to children[]
            new_node = Node(current_node, node_spot) # the parent node is the current node
            children.append(new_node)

        # traverse children[] and calculate the g, h, and f costs of each child and add to open list
        for child in children:
            
            child.gcost = current_node.gcost + 1
            child.hcost = abs(end_node.position[0] - child.position[0]) + abs(end_node.position[1] - child.position[1]) # manhattan distance
            child.fcost = child.gcost + child.hcost

            # check if the child is already in the open list
            isInOpen = False
            for check_node in open_spots:
                if child.position == check_node.position:
                    isInOpen = True

            # if child is in the open list, move on to the next child in children
            if isInOpen == True:
                continue
            
            # if child not in open list, add it to the open list
            heapq.heappush(open_spots, child)
            
    #
    return None

def mazeCreate():
    
    maze = [
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
]

    
    start = (0,0)
    end = (len(maze)-1, len(maze[0])-1)

    mazeRun(maze, start, end)


def mazeRun(maze, start, end):
    path = astar(maze, start, end)

    if not isinstance(path, list):
        print("ERROR")
        return
    else:
        for spot in path:
          maze[spot[0]][spot[1]] = 2

    for row in maze:
        line = []
        for col in row:
          if col == 1:
            line.append("\u2588") #unicode character for a filled in block
          elif col == 0:
            line.append(" ")
          elif col == 2:
            line.append(".")
        print("".join(line))

    print(path)

if __name__ == "__main__":
    mazeCreate()
