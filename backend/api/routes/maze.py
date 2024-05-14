from flask import jsonify
from api import app
import random
class Coords:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __repr__(self):
        return f"Coords(X={self.X}, Y={self.Y})"

@app.route("/api/test_maze_solution", methods=["GET"])
def get_test_maze_solution():
    solution_length = random.randint(1, 10)
    maze_width = maze_height = 3
    
    characters = ['0', '1']
    
    path = []
    for _ in range(solution_length):
        state = [[random.choice(characters) for _ in range(maze_width)] for _ in range(maze_height)]
        
        path.append(state)
    
    print(path)
    return path
@app.route("/api/make_maze_sparse/<int:dim1>/<int:dim2>", methods=["GET"])
def make_maze_sparse(dim1, dim2):
    maze = [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
        ['1', '0', '1', '0', '1', '0', '1', '1', '0', '1'],
        ['1', '0', '1', '0', '1', '0', '0', '1', '0', '1'],
        ['1', '0', '1', '0', '1', '1', '0', '1', '0', '1'],
        ['1', '0', '1', '0', '0', '0', '0', '1', '0', '1'],
        ['1', '0', '1', '0', '1', '1', '0', '1', '0', '1'],
        ['1', '0', '0', 'X', '0', '0', '0', '0', '0', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
    ]
    coord = Coords(1,1)
    get_neighbors(maze,coord)
    return jsonify(maze)

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
    print(neighbors)
    return neighbors

#def recursive_helper(maze,visited):
