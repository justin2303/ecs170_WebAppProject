const serverUrl = 'http://localhost:5000';

function get_res() {
    fetch(`${serverUrl}/api/test_maze_solution`)
    .then(response => {
        console.log(response.json())
    })
}

function make_sparse() {
    document.getElementById("fetchButton").disabled = true;

    setTimeout(() => {
        document.getElementById("fetchButton").disabled = false;
    }, 100);

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

        const aStarSolution = await getAStarSolution(data.maze, data.start_coords, data.end_coords);
        const dijkstraSolution = await getDijkstraSolution(data.maze, data.start_coords, data.end_coords);
        const beamSearchSolution = await getBeamSearchSolution(data.maze, data.start_coords, data.end_coords, 20);

        animateSolutions(aStarSolution, dijkstraSolution, beamSearchSolution);
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
        return data;
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
        return data;
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
        return data;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

async function animateSolution(solution, color, executionTime) {
    const canvas = document.querySelector("#mazeContainer canvas");
    const context = canvas.getContext("2d");
    const cellSize = 10;
    let step = 0;

    const totalTime = executionTime * 1000;
    const animationSpeed = totalTime / solution.length;

    return new Promise(resolve => {
        const interval = setInterval(() => {
            if (step < solution.length) {
                const [row, col] = solution[step];
                const x = col * cellSize;
                const y = row * cellSize;
                context.fillStyle = color;
                context.fillRect(x, y, cellSize, cellSize);
                step++;
            } else {
                clearInterval(interval);
                resolve();
            }
        }, animationSpeed);
    });
}

async function animateSolutions(aStarSolution, dijkstraSolution, beamSearchSolution) {
    const aStarTime = aStarSolution.timeElapsed;
    const dijkstraTime = dijkstraSolution.timeElapsed;
    const beamSearchTime = beamSearchSolution.timeElapsed;

    const totalTime = aStarTime + dijkstraTime + beamSearchTime;
    const aStarRatio = aStarTime / totalTime;
    const dijkstraRatio = dijkstraTime / totalTime;
    const beamSearchRatio = beamSearchTime / totalTime;
    const maxTimeSeconds = document.getElementById("maxTime").value;

    await Promise.all([
        animateSolution(aStarSolution.solution, "rgba(0, 0, 255, 0.5)", maxTimeSeconds * aStarRatio),
        animateSolution(dijkstraSolution.solution, "rgba(0, 255, 0, 0.5)", maxTimeSeconds * dijkstraRatio),
        animateSolution(beamSearchSolution.solution, "rgba(255, 165, 0, 0.5)", maxTimeSeconds * beamSearchRatio)
    ]);

    stopTimer();
}

let startTime;
let timerInterval;

function startTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        document.getElementById("timer").innerText = "00:00:00.000";
    }
    startTime = Date.now();
    timerInterval = setInterval(updateTimer, 1);
    
    make_sparse();
}

function updateTimer() {
    const elapsedTime = Date.now() - startTime;
    let milliseconds = Math.floor(elapsedTime % 1000);
    let seconds = Math.floor((elapsedTime / 1000) % 60);
    let minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
    let hours = Math.floor((elapsedTime / (1000 * 60 * 60)) % 24);

    const formattedTime = 
        (hours < 10 ? "0" + hours : hours) + ":" +
        (minutes < 10 ? "0" + minutes : minutes) + ":" +
        (seconds < 10 ? "0" + seconds : seconds) + "." +
        (milliseconds < 10 ? "00" + milliseconds : milliseconds < 100 ? "0" + milliseconds : milliseconds);

    document.getElementById("timer").innerText = formattedTime;
}

function stopTimer() {
    clearInterval(timerInterval);
}