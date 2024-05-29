const serverUrl = 'http://localhost:5000';

function get_res() {
    fetch(`${serverUrl}/api/test_maze_solution`)
    .then(response => {
        console.log(response.json())
    })
}

function make_sparse() {
    var numRows = document.getElementById("N_rows").value;
    var numCols = document.getElementById("N_Cols").value;
    console.log("numRows:", numRows);
    console.log("numCols:", numCols);
    const url = `${serverUrl}/api/make_maze_sparse/${numRows}/${numCols}`;

    // Make the GET request to the Flask endpoint
    fetch(url)
    .then(response => {
        // Parse the JSON response
        return response.json();
    })
    .then(async data => {
        // Do something with the JSON data returned from the Flask endpoint
        drawMaze(data.maze, data.start_coords, data.end_coords);

        // Move these elsewhere
        // This is just for demoing
        const aStarSolution = await getAStarSolution(data.maze, data.start_coords, data.end_coords);
        console.log(aStarSolution);

        const dijkstraSolution = await getDijkstraSolution(data.maze, data.start_coords, data.end_coords);
        console.log(dijkstraSolution);

        const beamSearchSolution = await getBeamSearchSolution(data.maze, data.start_coords, data.end_coords, 20);
        console.log(beamSearchSolution)
    })
    .catch(error => {
        // Handle any errors that occur during the fetch request
        console.error('Error:', error);
    });
}

// Define your maze as a 2D array of 1s and 0s
function drawMaze(maze, start_coords, end_coords) {
    
    const canvas = document.createElement("canvas")
    const ctx = canvas.getContext("2d")
    
    // Define cell size and wall color
    const cellSize = 10
    const wallColor = "black"
    const freeSpaceColor = "white"
    canvas.width = cellSize*maze[0].length // Set canvas width
    canvas.height = cellSize*maze.length // Set canvas height
    // Function to draw the maze
    for (let row = 0; row < maze.length; row++) {
        for (let col = 0; col < maze[row].length; col++) {
            const x = col * cellSize
            const y = row * cellSize

            // Draw walls for 1s
            if (maze[row][col] === 1) {
                ctx.fillStyle = wallColor
                ctx.fillRect(x, y, cellSize, cellSize)
            } else { // Draw free spaces for 0s
                ctx.fillStyle = freeSpaceColor
                ctx.fillRect(x, y, cellSize, cellSize)
            }
        }
    }

    const x1 = start_coords[1] * cellSize;
    const y1 = start_coords[0] * cellSize;
    ctx.fillStyle = "red";
    ctx.fillRect(x1, y1, cellSize, cellSize);


    const x2 = end_coords[1] * cellSize;
    const y2 = end_coords[0] * cellSize;
    ctx.fillStyle = "yellow";
    ctx.fillRect(x2, y2, cellSize, cellSize);

    const mazeContainer = document.getElementById("mazeContainer")
    mazeContainer.innerHTML = ""//set empty.
    mazeContainer.appendChild(canvas)
}//make maze

function test_neighbors() {
    
}

async function getAStarSolution(maze, start_coords, end_coords) {
    return fetch(`${serverUrl}/api/algorithm/astar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maze: maze,
            start_coords: start_coords,
            end_coords: end_coords
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        const solution = data.solution;
        return solution;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

async function getDijkstraSolution(maze, start_coords, end_coords) {
    return fetch(`${serverUrl}/api/algorithm/dijkstra`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maze: maze,
            start_coords: start_coords,
            end_coords: end_coords
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        const solution = data.solution;
        return solution;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

async function getBeamSearchSolution(maze, start_coords, end_coords, beam_width = 20) {
    return fetch(`${serverUrl}/api/algorithm/beam_search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maze: maze,
            start_coords: start_coords,
            end_coords: end_coords,
            beam_width: beam_width
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        const solution = data.solution;
        return solution;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}