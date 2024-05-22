from api import app
from flask import request

@app.route("/api/algorithm/beam_search", methods=["POST"])
def solve_maze_beam_search():
    maze = request.json.get('maze')
    pass


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
        

def beam_search(grid, start_node, goal_node, beam_width):
    # Implement beam search to find a path from start to goal
    # Placeholder for actual beam search logic
    pass

#Prints maze by taking grid of nodes as a parameter, prints Xs for walls, Os for path
def print_maze(grid):
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        for x in range(width):
            if(grid[y][x].is_wall):
                print('X', end='  ')
            else:
                print('O', end='  ')
        print(end='\n\n')


def main():
    layout = [
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0]
    ]

    grid = create_nodes_grid(layout)
    print_maze(grid)
    

if __name__ == "__main__":
    main()