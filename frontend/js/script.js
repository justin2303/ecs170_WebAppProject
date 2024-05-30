const serverUrl = 'http://localhost:5000';

function generate_maze() {
    stopTimer();
    document.getElementById("fetchButton").disabled = true;

    setTimeout(() => {
        document.getElementById("fetchButton").disabled = false;
    }, 100);

    var numRows = document.getElementById("N_rows").value;
    var numCols = document.getElementById("N_Cols").value;
    console.log("numRows:", numRows);
    console.log("numCols:", numCols);
    const url = `${serverUrl}/api/maze/generate/${numRows}/${numCols}`;

    // Make the GET request to the Flask endpoint
    fetch(url)
    .then(response => {
        // Parse the JSON response
        return response.json();
    })
    .then(async data => {
        // Do something with the JSON data returned from the Flask endpoint
        drawMaze(data.maze, data.start_coords, data.end_coords);

        const aStarData = await getAStarData(data.maze, data.start_coords, data.end_coords);
        const dijkstraData = await getDijkstraData(data.maze, data.start_coords, data.end_coords);
        const beamSearchData = await getBeamSearchData(data.maze, data.start_coords, data.end_coords, 20);

        startTimer();
        await animateSolutions(aStarData, dijkstraData, beamSearchData);
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

async function getAStarData(maze, start_coords, end_coords) {
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

async function getDijkstraData(maze, start_coords, end_coords) {
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

async function getBeamSearchData(maze, start_coords, end_coords, beam_width = 20) {
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

async function animateSolutions(aStarData, dijkstraData, beamSearchData) {
    const aStarTime = aStarData.timeElapsed;
    const dijkstraTime = dijkstraData.timeElapsed;
    const beamSearchTime = beamSearchData.timeElapsed;

    const totalTime = aStarTime + dijkstraTime + beamSearchTime;
    const aStarRatio = aStarTime / totalTime;
    const dijkstraRatio = dijkstraTime / totalTime;
    const beamSearchRatio = beamSearchTime / totalTime;
    const maxTimeSeconds = document.getElementById("maxTime").value;

    const aStarSimTimeElapsed = maxTimeSeconds * aStarRatio;
    const dijkstraSimTimeElapsed = maxTimeSeconds * dijkstraRatio;
    const beamSearchSimTimeElapsed = maxTimeSeconds * beamSearchRatio;

    await Promise.all([
        animateSolution(aStarData.solution, "rgba(0, 0, 255, 0.5)", aStarSimTimeElapsed),
        animateSolution(dijkstraData.solution, "rgba(0, 255, 0, 0.5)", dijkstraSimTimeElapsed),
        animateSolution(beamSearchData.solution, "rgba(255, 165, 0, 0.5)", beamSearchSimTimeElapsed)
    ]);

    stopTimer();

    console.log("A*: # of Steps =", aStarData.solution.length, "| Sim Time Elapsed (s) =", aStarSimTimeElapsed, "| Actual Time Elapsed (s) =", aStarData.timeElapsed);
    console.log("Dijkstra: # of Steps =", dijkstraData.solution.length, "| Sim Time Elapsed (s) =", dijkstraSimTimeElapsed, "| Actual Time Elapsed (s) =", dijkstraData.timeElapsed);
    console.log("Beam Search: # of Steps =", beamSearchData.solution.length, "| Sim Time Elapsed (s) =", beamSearchSimTimeElapsed, "| Actual Time Elapsed (s) =", beamSearchData.timeElapsed);
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
