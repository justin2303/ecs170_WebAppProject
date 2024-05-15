from flask import jsonify
from api import app
import random
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
    #for now ignore dim1dim2
    maze = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append('1')
        maze.append(row)
    #10x10 maze with 1s
    random_start =  Coords(random.randint(0, 9),random.randint(0, 9))
    maze[random_start.Y][random_start.X]='X'
    visited =[]
    spaces = 60
    recursive_helper(maze,visited,random_start, spaces)
    #coord = Coords(1,1)
    #get_neighbors(maze,coord)
    #print(Coords(1,1)==Coords(1,2))
    #print(Coords(1,1)==Coords(1,1))
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

def recursive_helper(maze,visited,current, spaces):
    if spaces<=0:
        print("setting endpos")
        maze[current.Y][current.X]='Y'
        return maze
    visited.append(current)
    nexts = get_neighbors(maze, current)
    print("got here1")
    index = random.randint(0, len(nexts)-1)
    found = False
    count = 0
    print("got here2")
    current = nexts[index]
    for x in range(0, len(nexts)):
        if(len(visited)==1 or found):
            break
        for y in range(0, len(visited)):
            if visited[y]==current:
                count += 1
                if(count==len(nexts)):
                    print("found loop, ending prematurely..")
                    maze[current.Y][current.X]='Y'
                    return maze
                if(index==len(nexts)-1):
                    index=0
                else:
                    index +=1
                current = nexts[index]
                break
            if y== len(visited)-1:
                found = True
    #found an unvisited node
    maze[current.Y][current.X]='0'
    print("got here3")
    recursive_helper(maze,visited,current, spaces-1)
    return maze
    



            


    