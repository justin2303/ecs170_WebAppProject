import time
from flask import request, jsonify
from api import app

@app.route("/api/algorithm/beam_search", methods=["POST"])
def solve_maze_beam_search():
    maze = request.json.get('maze')
    start_coords = tuple(request.json.get('start_coords'))
    end_coords = tuple(request.json.get('end_coords'))
    beam_width = request.json.get('beam_width')

    if beam_width is None:
        beam_width = 20

    try:
        grid = create_nodes_grid(maze)
        start_node = grid[start_coords[0]][start_coords[1]]
        goal_node = grid[end_coords[0]][end_coords[1]]

        start_time = time.perf_counter()
        path = beam_search(grid, start_node, goal_node, beam_width)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        solution = []
        for node in path:
            solution.append((node.y, node.x))

        if not solution:
            raise Exception("No path")
    except Exception as e:
        return jsonify( {'error': str(e)} ), 400
    
    return jsonify({ 'solution': solution, 'timeElapsed': elapsed_time }), 200

# Harinderjit Malhi
from api.utils.node import Node

# Variable "layout": a 2D list of 0s and 1s
# Purpose of function: create a 2D list of nodes based on the 0s and 1s
def create_nodes_grid(layout):
    # Extract heights and widths
    height = len(layout)
    if height > 0:
        width = len(layout[0])
    else:
        width = 0

    grid = []
    for y in range(height):
        new_grid_row = []   # Create row in which to place nodes in 

        for x in range(width):
            if layout[y][x] == 1:  # If layout contains 1, pretend node is a wall
                is_wall = True
                new_node = Node(x, y, is_wall)
            else:                         
                is_wall = False
                new_node  = Node(x, y, is_wall)

            new_grid_row.append(new_node)  #Place node in grid row
        
        #Once row at y nodes have been processed, append entire row of nodes to grid
        grid.append(new_grid_row)
    
    return grid


# Variable "current_node": starting node for calculation
# variable  "goal_node": node to which reach on maze
# Heuristic function (Uses manhattan Distance)
def manhattan_distance(current_node, goal_node):
    horizontal_dist = abs(goal_node.x - current_node.x)
    vertical_dist = abs(goal_node.y - current_node.y)
    return horizontal_dist + vertical_dist

# Function to produce nearest neighbors to a node
# Variable "grid": holds 2D list of nodes
# Variable "current_node": node whose neighbors we will get
def adjacent_neighbors(current_node, grid):
    # Directions: up, down, right, left = (-1,0), (1,0),  (0, 1), (0,1)
    #Calculate adjacent nodes
    neighbor_coordinates = [
        (current_node.y - 1, current_node.x + 0),   #Up coordinates
        (current_node.y + 1, current_node.x + 0),   #Down coordinates
        (current_node.y + 0,  current_node.x + 1),  #Right coordinates
        (current_node.y + 0,  current_node.x - 1)   #Left coordinates
    ]

    # Get height and width of grid
    max_height = len(grid)
    max_width = len(grid[0])
    neighbors = []

    for neighbor in neighbor_coordinates:
        #Only keep non-wall neighbor nodes within bounds 
        neighbor_y, neighbor_x = neighbor[0], neighbor[1]
        if 0 <= neighbor_y < max_height and 0 <= neighbor_x < max_width and not grid[neighbor_y][neighbor_x].is_wall:
            neighbors.append(grid[neighbor_y][neighbor_x])

    return neighbors


# Function to calculate the full cost for a node
def calculate_full_cost(node, goal_node):
        return node.cost + manhattan_distance(node, goal_node)

#Returns "best node", AKA the node that has shortest dist to goal and has shortest cost thus far
#Parameter list: list of nodes
#parameter goal_node: the node to reach and compare distances with
def closest_node(list, goal_node):
    shortest_path = float('inf')
    best_node = None
    
    for node in list:
        total_dist = calculate_full_cost(node, goal_node)
        if shortest_path > total_dist:
            shortest_path = total_dist
            best_node = node

    return best_node


def trim_open_list(open_list, beam_width, goal_node):
    # Early exit if trimming is not needed
    if len(open_list) <= beam_width:
        return open_list

    # Create a list to store the indices of the nodes with the lowest full cost
    selected_indices = []

    # Iterate to select the top 'beam_width' nodes based on their full cost
    for _ in range(min(beam_width, len(open_list))):
        min_cost = float('inf')
        min_index = -1
        for i in range(len(open_list)):
            # Calculate full cost only if the node is not already selected
            if i not in selected_indices:
                full_cost = calculate_full_cost(open_list[i], goal_node)
                if full_cost < min_cost:
                    min_cost = full_cost
                    min_index = i
        if min_index != -1:
            selected_indices.append(min_index)

    # Construct a new open list from the selected indices
    new_open_list = [open_list[i] for i in selected_indices]
    return new_open_list


# Implement beam search to find a path from start to goal
def beam_search(grid, start_node, goal_node, beam_width):
    closed_list = []
    open_list = []
    path = []
    #Add start_node to closed list and initialize its G cost
    start_node.cost = 0
    open_list.append(start_node)

    while len(open_list) > 0:
        best_node = closest_node(open_list, goal_node)
        open_list.remove(best_node)
        closed_list.append(best_node)
        best_node.explored = True  # Mark node as explored


        if best_node == goal_node:
            #Backtrack to reconstruct th path
            current_node = best_node
            while current_node != None:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]
        
        neighbors = adjacent_neighbors(best_node, grid)
        for neighbor in neighbors:

            if (neighbor not in closed_list) and (neighbor not in open_list):
                neighbor.parent = best_node #Set the parent
                neighbor.cost = best_node.cost + 1 #Maze steps count as 1 in terms of steps
                open_list.append(neighbor)
            elif neighbor in open_list:
                #If node had already been encountered by another "parent", chek if setting best_node as its parent
                #   create a more efficient overall cost
                if(best_node.cost + 1 < neighbor.cost):
                    neighbor.parent = best_node
                    neighbor.cost = best_node.cost + 1
        
        #Function to keep the search trimmed to beam width
        open_list = trim_open_list(open_list, beam_width, goal_node)
    
    return path

#Prints maze by taking grid of nodes as a parameter, prints Xs for walls, Os for path
def print_maze(grid):
    height = len(grid)
    width = len(grid[0])

    #Collect path nodes for marking
    path_nodes = set()
    for row in grid:
        for node in row:
            if node.parent is not None:
                path_nodes.add((node.x, node.y))

    for y in range(height):
        for x in range(width):
            if grid[y][x].is_wall:
                print('X', end=' ') #Walls
            elif (x, y) in path_nodes:
                print('*', end=' ')  #Mark path nodes with *
            elif grid[y][x].explored:
                print('+', end=' ')  #Mark explored nodes
            else:
                print('O', end=' ') #Roads
        print()



def main():
    layout = [
        [0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    grid = create_nodes_grid(layout)
    print("Initial Maze:")
    print_maze(grid)
    
    start_node = grid[0][0]
    goal_node = grid[9][9]
    beam_width = 20

    path = beam_search(grid, start_node, goal_node, beam_width)
    
    print("\nMaze After Beam Search:")
    print_maze(grid)
    
    if path:
        print("\nPath Found:")
        for node in path:
            print(f"({node.x}, {node.y})")
    else:
        print("\nNo Path Found.")

if __name__ == "__main__":
    main()