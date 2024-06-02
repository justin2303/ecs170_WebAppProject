from api import app
import numpy as np

def getResult(test_app, algorithm_name, maze_data):
    response = test_app.post(f"/api/algorithm/{algorithm_name}", json=maze_data)
    json_response = response.json
    return json_response['solution'], json_response['timeElapsed']

def find_smallest_ratio(times):
    arr = np.array(times)
    total_sum = np.sum(arr)
    ratios = arr / total_sum
    
    min_ratio_index = np.argmin(ratios)
    min_ratio = np.min(ratios)

    print(times)
    print(ratios)
    
    return min_ratio, min_ratio_index

def run_trials(num_trials, rows, cols):
    test_app = app.test_client()

    result = []
    fastest = [None, None, None]
    saved_maze = [None, None, None]

    for trial in range(num_trials):
        response = test_app.get(f"/api/maze/generate/{rows}/{cols}")
        maze_data = response.json

        astar = getResult(test_app=test_app, algorithm_name="astar", maze_data=maze_data)
        dijkstra = getResult(test_app=test_app, algorithm_name="dijkstra", maze_data=maze_data)
        beam_search = getResult(test_app=test_app, algorithm_name="beam_search", maze_data=maze_data)

        times = [astar[1], dijkstra[1], beam_search[1]]
        result.append(times)

        min_ratio, min_ratio_index = find_smallest_ratio(times)
        if fastest[min_ratio_index] is None or min_ratio < fastest[min_ratio_index]:
            fastest[min_ratio_index] = min_ratio
            saved_maze[min_ratio_index] = maze_data
    
    return result, fastest, saved_maze

def main():
    trial_results = run_trials(num_trials=50, rows=100, cols=100)
    print(trial_results[2][2])

if __name__ == "__main__":
    main()
