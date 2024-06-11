import unittest
from api import app
from api.utils.misc import display_maze

def generate_maze(rows, cols):
    test_app = app.test_client()
    response = test_app.get(f"/api/maze/generate/{rows}/{cols}")
    maze_data = response.json
    display_maze(maze_data)
    return maze_data

maze_data = generate_maze(50, 50)

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.maze_data = maze_data

    def display_results(self, algorithm_name, algorithm_data):
        print(algorithm_name)
        print("\tSolution:", algorithm_data["solution"])
        print("\tExecution Time:", algorithm_data["timeElapsed"], "s")

    def test_generate_maze(self):
        rows, cols = 50, 50
        response = self.app.get(f"/api/maze/generate/{rows}/{cols}")
        self.assertEqual(response.status_code, 200)

    def test_solve_maze_astar(self):
        response = self.app.post("/api/algorithm/astar", json=self.maze_data)
        self.assertEqual(response.status_code, 200)
        json_data = response.json
        self.display_results("A*", json_data)

    def test_solve_maze_dijkstra(self):
        response = self.app.post("/api/algorithm/dijkstra", json=self.maze_data)
        self.assertEqual(response.status_code, 200)
        json_data = response.json
        self.display_results("Dijkstra", json_data)

    def test_solve_maze_beam_search(self):
        response = self.app.post("/api/algorithm/beam_search", json=self.maze_data)
        self.assertEqual(response.status_code, 200)
        json_data = response.json
        self.display_results("Beam Search", json_data)

if __name__ == '__main__':
    unittest.main()
