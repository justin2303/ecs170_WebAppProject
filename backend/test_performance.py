import threading
from api import app
import matplotlib.pyplot as plt

def trial(rows, cols, results):
    test_app = app.test_client()

    maze_response = test_app.get(f"/api/maze/generate/{rows}/{cols}")
    if maze_response.status_code != 200:
        return

    maze_data = maze_response.json

    astar_response = test_app.post("/api/algorithm/astar", json=maze_data)
    if astar_response.status_code != 200:
        return

    astar_data = astar_response.json

    dijkstra_response = test_app.post("/api/algorithm/dijkstra", json=maze_data)
    if dijkstra_response.status_code != 200:
        return

    dijkstra_data = dijkstra_response.json

    maze_data["beam_width"] = 3
    beam_search_response = test_app.post("/api/algorithm/beam_search", json=maze_data)
    if beam_search_response.status_code != 200:
        return

    beam_search_data = beam_search_response.json

    result = {
        "A*": {"steps": len(astar_data["solution"]), "time": astar_data["timeElapsed"]},
        "Dijkstra": {"steps": len(dijkstra_data["solution"]), "time": dijkstra_data["timeElapsed"]},
        "Beam Search": {"steps": len(beam_search_data["solution"]), "time": beam_search_data["timeElapsed"]}
    }

    results[(rows, cols)].append(result)

def simulate_trials(num_trials, sizes):
    results = {}

    def run_trial(size):
        rows, cols = size
        results[size] = []
        print(f"Simulating {num_trials} mazes of size {rows}x{cols}...")
        for _ in range(num_trials):
            trial(rows, cols, results)

    threads = []
    for size in sizes:
        thread = threading.Thread(target=run_trial, args=(size,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results

def calculate_averages(trial_results):
    averages = {}

    for maze_size, trials in trial_results.items():
        total_steps = {"A*": 0, "Dijkstra": 0, "Beam Search": 0}
        total_time = {"A*": 0, "Dijkstra": 0, "Beam Search": 0}

        for trial in trials:
            for algorithm, data in trial.items():
                total_steps[algorithm] += data["steps"]
                total_time[algorithm] += data["time"]

        avg_steps = {algorithm: total_steps[algorithm] / len(trials) for algorithm in total_steps}
        avg_time = {algorithm: total_time[algorithm] / len(trials) for algorithm in total_time}

        averages[maze_size] = {"steps": avg_steps, "time": avg_time}

    return averages

def plot_average_steps(axes, averages):
    algorithms = ["A*", "Dijkstra", "Beam Search"]
    bar_width = 0.2

    for i, algorithm in enumerate(algorithms):
        algorithm_values = [averages[size]["steps"][algorithm] for size in averages.keys()]
        maze_sizes = [f"{size[0]}x{size[1]}" for size in averages.keys()]
        x = [index + i * bar_width for index in range(len(maze_sizes))]
        axes.bar(x, algorithm_values, width=bar_width, label=algorithm)
    axes.set_xlabel("Maze Size")
    axes.set_ylabel("Steps")
    axes.set_title("Average Steps per Maze Size")
    axes.set_xticks([index + bar_width for index in range(len(maze_sizes))])
    axes.set_xticklabels(maze_sizes, rotation=90)
    axes.legend()

def plot_average_time(axes, averages):
    algorithms = ["A*", "Dijkstra", "Beam Search"]
    bar_width = 0.2

    for i, algorithm in enumerate(algorithms):
        algorithm_values = [averages[size]["time"][algorithm] for size in averages.keys()]
        maze_sizes = [f"{size[0]}x{size[1]}" for size in averages.keys()]
        x = [index + i * bar_width for index in range(len(maze_sizes))]
        axes.bar(x, algorithm_values, width=bar_width, label=algorithm)
    axes.set_xlabel("Maze Size")
    axes.set_ylabel("Time (s)")
    axes.set_title("Average Time per Maze Size")
    axes.set_xticks([index + bar_width for index in range(len(maze_sizes))])
    axes.set_xticklabels(maze_sizes, rotation=90)
    axes.legend()

def plot_average_cost(axes, averages):
    algorithms = ["A*", "Dijkstra", "Beam Search"]
    largest_maze_size = list(averages.keys())[-1]
    largest_maze_averages = averages[largest_maze_size]

    for algorithm in algorithms:
        steps = largest_maze_averages["steps"][algorithm]
        time = largest_maze_averages["time"][algorithm]

        cost_per_step_values = [0.001 * i for i in range(1, 151)]
        total_cost_values = [time + steps * cost for cost in cost_per_step_values]

        axes.plot(cost_per_step_values, total_cost_values, label=algorithm)

    axes.set_xlabel("Cost per Step (s)")
    axes.set_ylabel("Total Cost = Time + Step * Cost per Step (s)")
    axes.set_title(f"Total Average Cost vs Cost per Step for Maze Size {largest_maze_size[0]}x{largest_maze_size[1]}")
    axes.legend()

def main():
    num_trials = 50
    start_size = 5
    end_size = 105
    increment = 20

    maze_sizes = []
    current_maze_size = (start_size, start_size)
    while current_maze_size[1] <= end_size:
        maze_sizes.append(current_maze_size)
        
        if current_maze_size[0] == current_maze_size[1]:
            current_maze_size = (current_maze_size[0], current_maze_size[1] + increment)
        else:
            current_maze_size = (current_maze_size[0] + increment, current_maze_size[1])

    trial_results = simulate_trials(num_trials, maze_sizes)
    averages = calculate_averages(trial_results)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    plot_average_steps(axes[0], averages)
    plot_average_time(axes[1], averages)
    plot_average_cost(axes[2], averages)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
