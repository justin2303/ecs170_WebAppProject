from flask import jsonify
from api import app
import random
import queue
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
    maze = make_prims_maze(dim1,dim2)
    return jsonify(maze)

def make_rand_maze():
#for now ignore dim1dim2
    maze = []
    for i in range(30):
        row = []
        for j in range(30):
            row.append('1')
        maze.append(row)
    #10x10 maze with 1s
    random_start =  Coords(random.randint(0, 9),random.randint(0, 9))
    maze[random_start.Y][random_start.X]='X'
    visited =[]
    spaces = 80
    print("rand start: ", random_start)
    maze, current =recursive_helper(maze,visited,random_start, spaces)
    #coord = Coords(1,1)
    #get_neighbors(maze,coord)
    #print(Coords(1,1)==Coords(1,2))
    #print(Coords(1,1)==Coords(1,1))
    print("current: ", current)
    print("distance: ",get_dist(random_start, current))
    return (maze,get_dist(random_start, current))

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

def recursive_helper(maze,visited,current, spaces):
    if spaces<=0:
        print("setting endpos")
        maze[current.Y][current.X]='Y'
        return maze,current
    visited.append(current)
    nexts = get_neighbors(maze, current)
    index = random.randint(0, len(nexts)-1)
    found = False
    count = 0
    next = nexts[index]
    for x in range(0, len(nexts)):
        if(len(visited)==1 or found):
            break
        for y in range(0, len(visited)):
            if visited[y]==next:
                count += 1
                if(count==len(nexts)):
                    print("found loop, ending prematurely..")
                    maze[next.Y][next.X]='Y'
                    return maze,next
                if(index==len(nexts)-1):
                    index=0
                else:
                    index +=1
                next = nexts[index]
                break
            if y== len(visited)-1:
                found = True
    #found an unvisited node
    maze[next.Y][next.X]='0'
    return recursive_helper(maze,visited,next, spaces-1)
def get_dist(start, current):
    print(start, current)
    return abs(start.X-current.X) + abs(start.Y-current.Y)

def recursive_opt(maze,visited,current, spaces):
    print("spaces: ", spaces)
    if spaces<=0:
        print("setting endpos")
        maze[current.Y][current.X]='Y'
        return maze
    visited.append(current)
    nexts = get_neighbors(maze, current)
    pq=queue.PriorityQueue()
    for next in nexts:
        pq.put((get_dist(visited[0], next), next))
    next_dist, next_node = pq.get()
    print("self: ",visited[0])
    print(next_node)
    found = False
    while(not found):
        for x in range(len(visited)):
            print(x)
            if visited[x] == next_node:
                if(pq.empty()):
                    print("circle found")
                    maze[current.Y][current.X]='Y'
                    return
                next_dist, next_node = pq.get()
                break
            if(x== len(visited)-1):
                found=True
    #found next node
    maze[next_node.Y][next_node.X]='0'
    spaces -= 1
    recursive_opt(maze,visited,next_node, spaces)
    return maze

#try prims.

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

def make_prims_maze(dim1,dim2):
    maze = []
    for i in range(dim1):
        row = []
        for j in range(dim2):
            row.append('1')
        maze.append(row)
    random_start =  Coords(random.randint(0, 29),random.randint(0, 29))
    maze[random_start.Y][random_start.X]='X'
    front = []
    next = get_frontier(maze,random_start)
    for x in next:
        front.append(x)
    while front:
        #get rand coord
        rand_index=random.randint(0, len(front)-1)
        curr_Coord=front[rand_index]
        front.pop(rand_index)
        maze[curr_Coord.Y][curr_Coord.X]='0'
        #now make passage
        passages = possible_passage(maze, curr_Coord)
        rand_passage = passages[random.randint(0, len(passages)-1)]
        maze[rand_passage.Y][rand_passage.X]='0'
        #repopulate front.
        next = get_frontier(maze,curr_Coord)
        if(len(next)==0 and len(front)==0):
            maze[rand_passage.Y][rand_passage.X]='Y'
        for x in next:
            front.append(x)
        print(curr_Coord)
    return maze
        

            


    