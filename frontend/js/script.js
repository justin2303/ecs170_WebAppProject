const serverUrl = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("fetchButton").disabled = false;
    document.getElementById("fetchButton2").disabled = true;
});

function reset() {
    stopTimer();
    document.getElementById("fetchButton").disabled = true;
    document.getElementById("fetchButton2").disabled = true;
    document.getElementById("time-scoreboard").innerHTML='';
    document.getElementById("steps-scoreboard").innerHTML='';
}

let lastMazeData = null;

function generateMaze() {
    reset();

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
        const aStarData = await getAStarData(data.maze, data.start_coords, data.end_coords);
        const dijkstraData = await getDijkstraData(data.maze, data.start_coords, data.end_coords);
        const beamSearchData = await getBeamSearchData(data.maze, data.start_coords, data.end_coords, parseInt(document.getElementById("beamWidth").value));

        drawMaze(data.maze, data.start_coords, data.end_coords);
        await animateSolutions(aStarData, dijkstraData, beamSearchData);

        lastMazeData = data;
        document.getElementById("fetchButton").disabled = false;
        document.getElementById("fetchButton2").disabled = false;
    })
    .catch(error => {
        console.error(error);
        generateMaze();
    });
}

async function redoLastMaze() {
    reset();

    const data = lastMazeData;
    drawMaze(data.maze, data.start_coords, data.end_coords);
    const aStarData = await getAStarData(data.maze, data.start_coords, data.end_coords);
    const dijkstraData = await getDijkstraData(data.maze, data.start_coords, data.end_coords);
    const beamSearchData = await getBeamSearchData(data.maze, data.start_coords, data.end_coords, parseInt(document.getElementById("beamWidth").value));
    await animateSolutions(aStarData, dijkstraData, beamSearchData);

    document.getElementById("fetchButton").disabled = false;
    document.getElementById("fetchButton2").disabled = false;
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

    startTimer();
    await Promise.all([
        animateSolution(aStarData.solution, "rgba(0, 0, 255, 0.5)", aStarSimTimeElapsed), // blue
        animateSolution(dijkstraData.solution, "rgba(0, 255, 0, 0.5)", dijkstraSimTimeElapsed), // green
        animateSolution(beamSearchData.solution, "rgba(255, 165, 0, 0.5)", beamSearchSimTimeElapsed) // orange
    ]);
    stopTimer();

    const solutions = [
        { name: "A*", time: aStarSimTimeElapsed, steps: aStarData.solution.length },
        { name: "Dijkstra", time: dijkstraSimTimeElapsed, steps: dijkstraData.solution.length },
        { name: "Beam Search", time: beamSearchSimTimeElapsed, steps: beamSearchData.solution.length }
    ];

    const timeScoreboard = document.getElementById("time-scoreboard");
    const stepsScoreboard = document.getElementById("steps-scoreboard");

    timeScoreboard.innerHTML = '';
    stepsScoreboard.innerHTML = '';

    solutions.sort((a, b) => a.time - b.time);
    solutions.forEach((solution, index) => {
        const div = document.createElement('div');
        div.textContent = `${index + 1}. ${solution.name}: ${solution.time.toFixed(3)} s`;
        timeScoreboard.appendChild(div);
    });

    solutions.sort((a, b) => a.steps - b.steps);
    solutions.forEach((solution, index) => {
        const div = document.createElement('div');
        div.textContent = `${index + 1}. ${solution.name}: ${solution.steps} steps`;
        stepsScoreboard.appendChild(div);
    });

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

function showScoreboard(type) {
    document.querySelectorAll('.scoreboard-tab').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));

    if (type === 'time') {
        document.getElementById('time-scoreboard').classList.add('active');
        document.querySelector('.tab-button[onclick="showScoreboard(\'time\')"]').classList.add('active');
    } else if (type === 'steps') {
        document.getElementById('steps-scoreboard').classList.add('active');
        document.querySelector('.tab-button[onclick="showScoreboard(\'steps\')"]').classList.add('active');
    }
}
