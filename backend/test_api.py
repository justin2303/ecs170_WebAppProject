import unittest
from api import app
from api.utils.misc import extract_maze_data, display_maze
import time

maze_data = None
list_mazes = []
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
    list_mazes.append(maze_data)


    #display_maze(maze_data)

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


def run_quick_test(x):#make 100 50x50 prims mazes and run tests
    test_app = app.test_client()
    response2 = test_app.post("/api/algorithm/astar", json=list_mazes[x])
    json_data1 = response2.json
    sol_buff = json_data1['solution']
    sol1 = [tuple(coords) for coords in sol_buff]
    response3 = test_app.post("/api/algorithm/dijkstra", json=list_mazes[x])
    json_data2 = response3.json
    sol_buff = json_data2['solution']
    sol2 = [tuple(coords) for coords in sol_buff]
    response4 = test_app.post("/api/algorithm/beam_search", json=list_mazes[x])
    json_data3= response4.json
    sol_buff = json_data3['solution']
    sol3 = [tuple(coords) for coords in sol_buff]
    count1=0
    count2=0
    count3= 0
    for _ in sol1:
        count1 +=1
    for _ in sol2:
        count2 +=1
    for _ in sol3:
        count3 +=1
    print(count1)
    print(count2)
    print(count3)

def test_dijkstra(x):
    test_app = app.test_client()
    start_time = time.time()
    response2 = test_app.post("/api/algorithm/dijkstra", json=list_mazes[x])
    end_time = time.time()
    total_time = end_time - start_time
    json_data1 = response2.json
    sol_buff = json_data1['solution']
    sol1 = [tuple(coords) for coords in sol_buff]
    count1=0
    for _ in sol1:
        count1 +=1
    return count1, total_time

def test_beam(x):
    test_app = app.test_client()
    start_time = time.time()
    response2 = test_app.post("/api/algorithm/beam_search", json=list_mazes[x])
    end_time = time.time()
    total_time = end_time - start_time
    json_data1 = response2.json
    sol_buff = json_data1['solution']
    sol1 = [tuple(coords) for coords in sol_buff]
    count1=0
    for _ in sol1:
        count1 +=1
    return count1, total_time


def test_astar(x):
    test_app = app.test_client()
    start_time = time.time()
    response2 = test_app.post("/api/algorithm/astar", json=list_mazes[x])
    end_time = time.time()
    total_time = end_time - start_time
    json_data1 = response2.json
    sol_buff = json_data1['solution']
    sol1 = [tuple(coords) for coords in sol_buff]
    count1=0
    for _ in sol1:
        count1 +=1
    return count1, total_time

if __name__ == '__main__':
    print("algorithm testing started!")
    for x in range (0,100):
        (generate_maze(100, 150))
    #unittest.main()
    total_moves1=0
    total_time1=0
    print("mazes generated!")
    for x in range (0,100):
        curr_move, curr_time =test_astar(x)
        total_moves1 += curr_move
        total_time1 += curr_time
    print(f"Astar algorithm, avg time: {total_time1/100} seconds, avg required moves: {total_moves1/100} moves")
    total_moves2=0
    total_time2=0
    for x in range (0,100):
        curr_move, curr_time =test_dijkstra(x)
        total_moves2 += curr_move
        total_time2 += curr_time
    print(f"Dijkstra algorithm, avg time: {total_time2/100} seconds, avg required moves: {total_moves2/100} moves")
    total_moves3=0
    total_time3=0
    for x in range (0,100):
        curr_move, curr_time =test_astar(x)
        total_moves3 += curr_move
        total_time3 += curr_time
    print(f"Beam Search algorithm, avg time: {total_time3/100} seconds, avg required moves: {total_moves3/100} moves")
    