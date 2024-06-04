import unittest
from api import app
from api.utils.misc import extract_maze_data, display_maze
import time
import threading
lock = threading.Lock()
results=[]
maze_data = None
list_mazes = []
def test_generate_maze(rows, cols):
    global maze_data
    test_app = app.test_client()
    response = test_app.get(f"/api/maze/generate/{rows}/{cols}")
    assert response.status_code == 200
    maze_data = response.get_json()
    list_mazes.append(maze_data)

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
def test_worker(x, results,y):
    alg=""
    test_app = app.test_client()
    total_time=0
    if(x==1):#astar
        alg="Astar"
        test_app = app.test_client()
        response2 = test_app.post("/api/algorithm/astar", json=list_mazes[y])
    elif x==2:#dijkstra
        alg="Dijkstra"
        test_app = app.test_client()
        response2 = test_app.post("/api/algorithm/dijkstra", json=list_mazes[y])
    else:#beam
        alg="Beam search"
        test_app = app.test_client()
        response2 = test_app.post("/api/algorithm/beam_search", json=list_mazes[y])
    lock.acquire()
    #print segment
    json_data1 = response2.json
    sol_buff = json_data1['solution']
    sol1 = [tuple(coords) for coords in sol_buff]
    count1=0
    for _ in sol1:
        count1 +=1
    total_time = json_data1['timeElapsed']
    #print(f"{alg} took {total_time} to finish and in {count1} moves!")
    results.append((alg, count1, total_time))
    lock.release()
    return count1, total_time
    

if __name__ == '__main__':
    print("algorithm testing started!")
    row=5
    col=5
    for x in range (0,50):
        (test_generate_maze(row, col))
        if row<col:
            row += 20
        else:
            col += 20
    total_moves1=0
    total_time1=0
    #testing mazes from small to large
    print("mazes generated!")
    row=5
    col=5
    for x in range (0,50):
        threads = []
        for i in range(3):
            thread = threading.Thread(target=test_worker, args=(i,results,x))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        #all done
        best=results[0]
        for a in range(3):
            if(results[a][2]<best[2]):
                best=results[a]
        print(f"for maze size {row}x{col}, here is the best: {best}")
        if row<col:
            row += 20
        else:
            col += 20
        results=[]
        
    #print(f"Astar algorithm, avg time: {total_time1/100} seconds, avg required moves: {total_moves1/100} moves")


    #
    """
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
    """