import time
from flask import request, jsonify
from api import app

@app.route("/api/algorithm/dijkstra", methods=["POST"])
def solve_maze_dijkstra():
    maze = request.json.get('maze')
    start_coords = tuple(request.json.get('start_coords'))
    end_coords = tuple(request.json.get('end_coords'))
    
    try:
        start_time = time.perf_counter()
        solution = dijkstra_solve_maze(maze, start_coords, end_coords)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        if not solution:
            raise Exception("No path")
    except Exception as e:
        return jsonify({ 'error': str(e)} ), 400
    
    return jsonify({ 'solution': solution, 'timeElapsed': elapsed_time }), 200


# Maia Burton
import heapq
import copy

def print_maze(maze):
    for row in maze:
        print(' '.join(str(x) for x in row))
        print()

def dijkstra_solve_maze(maze, start, end):
    
    # Initialize variables
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # up, down, left, right

    # Tracks the shortest distance to every node from the start node
    # Map every cell to default distance of infinity
    distances = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    
    distances[start] = 0
    priority_queue = [(0, start)]
    predecessors = { start: None }

    # Process to visualize the path
    maze_with_path = copy.deepcopy(maze)
    
    while priority_queue:
        current_distance, (row, col) = heapq.heappop(priority_queue)
        
        if (row, col) == end:
            break
        
        # Mark the current cell with 'X' and print the maze
        if maze_with_path[row][col] == 0:
            maze_with_path[row][col] = 'X'
        #print_maze(maze_with_path)

        # Iterate through the list of directions to calculate the neighboring cell's coordinates
        for dr, dc in directions:

            # coordinates of a neighboring cell relative to the current one (row, col)
            r, c = row + dr, col + dc   

            # Checks if the neighboring cell is a wall
            if 0 <= r < rows and 0 <= c < cols and maze[r][c] != 1:
                new_distance = current_distance + 1     # Calculates distance from starting point

                # Checks if the newly calculated distance between the neighbor cell and the start 
                # is less than the currently known distance for its neighbor
                    # If it's shorter, update the short distance and track the predecessor to 
                    # reconstruct the path later
                if new_distance < distances[(r, c)]:
                    distances[(r, c)] = new_distance
                    predecessors[(r, c)] = (row, col)

                    # Add the neighboring cell to the priority queue with the new distance as its priority
                    heapq.heappush(priority_queue, (new_distance, (r, c)))

    # Check if a path exists
    if distances[end] == float('inf'):
        print("No path exists from start to end")
        return None
    else:
        # Reconstruct the path and visualize the final path
        path = []
        step = end
        while step is not None:
            if maze_with_path[step[0]][step[1]] == 0:
                maze_with_path[step[0]][step[1]] = 'X'
            path.append(step)
            step = predecessors.get(step)
        path.reverse()

        #print("Final path:")
        #print_maze(maze_with_path)

        return path    

if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0]
    ]

    maze1 = [
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0]
    ]

    start = (0, 0)
    end = (4, 4)
    path = dijkstra_solve_maze(maze, start, end)
    print("Maze Path:", path)
    print()


    start = (0, 0)
    end = (19, 19)
    path = dijkstra_solve_maze(maze1, start, end)
    print("Maze1 Path:", path)



'''
Sources and References:

https://www.youtube.com/watch?v=EFg3u_E6eHU
https://www.youtube.com/watch?v=mbLzxKUeLJ4
'''
