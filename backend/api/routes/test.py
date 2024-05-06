from flask import jsonify
from api import app
import random

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
