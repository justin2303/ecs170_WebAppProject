import unittest
from api import app
from api.utils.misc import display_maze

maze_data = None

def generate_maze(rows, cols):
    global maze_data
    test_app = app.test_client()
    response = test_app.get(f"/api/make_maze_sparse/{rows}/{cols}")
    assert response.status_code == 200
    maze_data = response.get_json()
    display_maze(maze_data)

class TestApp(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = app.test_client()

    def test_solve_maze_astar(self):
        response = self.app.post("/api/algorithm/astar", json=maze_data)
        self.assertEqual(response.status_code, 200)
        print("A*:", response.get_json())

    def test_solve_maze_dijkstra(self):
        response = self.app.post("/api/algorithm/dijkstra", json=maze_data)
        self.assertEqual(response.status_code, 200)
        print("Dijkstra:", response.get_json())

    def test_solve_maze_beam_search(self):
        response = self.app.post("/api/algorithm/beam_search", json=maze_data)
        self.assertEqual(response.status_code, 200)
        print("Beam Search:", response.get_json())

if __name__ == '__main__':
    generate_maze(10, 10)
    unittest.main()
