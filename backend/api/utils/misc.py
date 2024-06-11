PLAYER = 'X'
GOAL = 'Y'

def extract_maze_data(maze_data):
    start_coords = None
    end_coords = None
    maze = []

    for i, row in enumerate(maze_data):
        maze_row = []
        for j, cell in enumerate(row):
            if cell == PLAYER:
                start_coords = [i, j]
                maze_row.append(0)
            elif cell == GOAL:
                end_coords = [i, j]
                maze_row.append(0)
            elif cell == '0':
                maze_row.append(0)
            elif cell == '1':
                maze_row.append(1)
        maze.append(maze_row)

    return maze, start_coords, end_coords

def display_maze(maze_data):
    maze = maze_data['maze']
    start_coords = tuple(maze_data['start_coords'])
    end_coords = tuple(maze_data['end_coords'])
    
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if (i, j) == start_coords:
                print(PLAYER, end=' ')
            elif (i, j) == end_coords:
                print(GOAL, end=' ')
            elif cell == 1:
                print('\u2588', end=' ')
            else:
                print(' ', end=' ')
        print()
