import random

from flask import jsonify
from api import app
from api.utils.misc import extract_maze_data

class Coords:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __repr__(self):
        return f"Coords(X={self.X}, Y={self.Y})"
    def __eq__(self, other):
        if isinstance(other, Coords):
            return self.X == other.X and self.Y == other.Y
        return False
    def __lt__(self, other):
        if isinstance(other, Coords):
            return self.X == other.X and self.Y == other.Y
        return False
    def __gt__(self, other):
        if isinstance(other, Coords):
            return self.X == other.X and self.Y == other.Y
        return False
    
@app.route("/api/maze/generate/<int:dim1>/<int:dim2>", methods=["GET"])
def generate_maze(dim1, dim2):
    maze = make_prims_maze(dim1,dim2)
    maze, start_coords, end_coords = extract_maze_data(maze)

    missing_data = []
    if maze is None:
        missing_data.append("Maze coordinates")
    if start_coords is None:
        missing_data.append("Start coordinates")
    if end_coords is None:
        missing_data.append("End coordinates")
    
    if missing_data:
        error_message = ", ".join(missing_data) + " are missing"
        print(error_message, "\n\n\n\n")
        return jsonify({'error': error_message}), 400

    maze_data = {
        'maze': maze,
        'start_coords': start_coords,
        'end_coords': end_coords
    }
    return jsonify(maze_data), 200

def get_neighbors(maze, coord):
    neighbors=[]
    if coord.X < len(maze[0]) - 1:
        new_coord = Coords(coord.X + 1, coord.Y)
        neighbors.append(new_coord)
    if coord.X > 0:
        new_coord = Coords(coord.X - 1, coord.Y)
        neighbors.append(new_coord)
    if coord.Y > 0:
        new_coord = Coords(coord.X , coord.Y-1)
        neighbors.append(new_coord)
    if coord.Y < len(maze) - 1:
        new_coord = Coords(coord.X , coord.Y + 1)
        neighbors.append(new_coord)
    return neighbors

def get_frontier(maze, coord):
    neighbors=[]
    if coord.X < len(maze[0]) - 2:
        new_coord = Coords(coord.X + 2, coord.Y)
        if(maze[new_coord.Y][new_coord.X]=='1'):#unexplored
            neighbors.append(new_coord)
    if coord.X > 1:
        new_coord = Coords(coord.X - 2, coord.Y)
        if(maze[new_coord.Y][new_coord.X]=='1'):
            neighbors.append(new_coord)
    if coord.Y > 1:
        new_coord = Coords(coord.X , coord.Y-2)
        if(maze[new_coord.Y][new_coord.X]=='1'):
            neighbors.append(new_coord)
    if coord.Y < len(maze) - 2:
        new_coord = Coords(coord.X , coord.Y + 2)
        if(maze[new_coord.Y][new_coord.X]=='1'):
            neighbors.append(new_coord)
    return neighbors

def possible_passage(maze, coord):
    neighbors=[]
    if coord.X < len(maze[0]) - 2:
        new_coord = Coords(coord.X + 2, coord.Y)
        if(maze[new_coord.Y][new_coord.X]!='1'):#explored exists a path.
            new_coord = Coords(coord.X+1 , coord.Y)
            neighbors.append(new_coord)
    if coord.X > 1:
        new_coord = Coords(coord.X - 2, coord.Y)
        if(maze[new_coord.Y][new_coord.X]!='1'):
            new_coord = Coords(coord.X -1 , coord.Y)
            neighbors.append(new_coord)
    if coord.Y > 1:
        new_coord = Coords(coord.X , coord.Y-2)
        if(maze[new_coord.Y][new_coord.X]!='1'):
            new_coord = Coords(coord.X , coord.Y - 1)
            neighbors.append(new_coord)
    if coord.Y < len(maze) - 2:
        new_coord = Coords(coord.X , coord.Y + 2)
        if(maze[new_coord.Y][new_coord.X]!='1'):
            new_coord = Coords(coord.X , coord.Y + 1)
            neighbors.append(new_coord)
    return neighbors

def make_prims_maze(dim1, dim2):
    maze = []
    for i in range(dim1):
        row = []
        for j in range(dim2):
            row.append('1')
        maze.append(row)
        
    random_start = Coords(random.randint(0, dim2-1), random.randint(0, dim1-1))
    maze[random_start.Y][random_start.X] = 'X'
    
    front = []
    next = get_frontier(maze, random_start)
    for x in next:
        front.append(x)
    
    while front:
        # Get random coordinate
        rand_index = random.randint(0, len(front)-1)
        curr_Coord = front[rand_index]
        front.pop(rand_index)
        maze[curr_Coord.Y][curr_Coord.X] = '0'
        
        # Now make passage
        passages = possible_passage(maze, curr_Coord)
        rand_passage = passages[random.randint(0, len(passages)-1)]
        maze[rand_passage.Y][rand_passage.X] = '0'
        
        # Repopulate front.
        next = get_frontier(maze, curr_Coord)
        if(len(next) == 0 and len(front) == 0):
            maze[rand_passage.Y][rand_passage.X] = 'Y'
        for x in next:
            front.append(x)
    
    maze = cleanup(maze)
    return maze


def cleanup(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j]!='1':
                continue
            temp = Coords(j,i)
            neighbors = get_neighbors(maze, temp)
            if(len(neighbors)!=4):
                continue
            tf = True
            for x in neighbors:
                #print(x.Y, x.X)
                if(maze[x.Y][x.X]=='1'):
                    tf=False
                    break
            #if any neighbosr are '1' forget it, else set to 0
            if tf:
                maze[i][j]='0' 

    return maze                   


"""
references: https://stackoverflow.com/questions/29739751/implementing-a-randomly-generated-maze-using-prims-algorithm
"""