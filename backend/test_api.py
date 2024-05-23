import unittest
from api import app
from api.utils.misc import extract_maze_data, display_maze

maze_data = None

def generate_maze(rows, cols):
    global maze_data
    test_app = app.test_client()
    response = test_app.get(f"/api/make_maze_sparse/{rows}/{cols}")
    assert response.status_code == 200
    maze_data = response.get_json()
    maze, start_coords, end_coords = extract_maze_data(maze_data)
    maze_data = {
        'maze': maze,
        'start_coords': start_coords,
        'end_coords': end_coords
    }
    display_maze(maze_data)

class TestApp(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = app.test_client()

    def test_solve_maze_astar(self):
        response = self.app.post("/api/algorithm/astar", json=maze_data)
        self.assertEqual(response.status_code, 200)
        print("Astar:", response.get_json())

    def test_solve_maze_dijkstra(self):
        response = self.app.post("/api/algorithm/dijkstra", json=maze_data)
        self.assertEqual(response.status_code, 200)
        print("Dijkstra:", response.get_json())

if __name__ == '__main__':
    generate_maze(10, 10)
    unittest.main()
