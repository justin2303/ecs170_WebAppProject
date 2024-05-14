

function get_res() {
    fetch("http://localhost:5000/api/test_maze_solution")
    .then(response => {
        console.log(response.json())
    })
}
function make_sparse() {
    var numRows = document.getElementById("N_rows").value;
    var numCols = document.getElementById("N_Cols").value;
    console.log("numRows:", numRows);
    console.log("numCols:", numCols);
    const url = `http://localhost:5000/api/make_maze_sparse/${numRows}/${numCols}`;

    // Make the GET request to the Flask endpoint
    fetch(url)
    .then(response => {
        // Parse the JSON response
        return response.json();
    })
    .then(data => {
        // Do something with the JSON data returned from the Flask endpoint
        drawMaze(data)
    })
    .catch(error => {
        // Handle any errors that occur during the fetch request
        console.error('Error:', error);
    });
}
const counter=0
// Define your maze as a 2D array of 1s and 0s
function drawMaze(maze) {
    
    const canvas = document.createElement("canvas")
    const ctx = canvas.getContext("2d")
    
    // Define cell size and wall color
    const cellSize = 20
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
            if (maze[row][col] === '1') {
                ctx.fillStyle = wallColor
                ctx.fillRect(x, y, cellSize, cellSize)
            }else if(maze[row][col] === 'X'){
                ctx.fillStyle = "red"
                ctx.fillRect(x, y, cellSize, cellSize)
            } 
            else { // Draw free spaces for 0s
                ctx.fillStyle = freeSpaceColor
                ctx.fillRect(x, y, cellSize, cellSize)
            }
        }
    }
    const mazeContainer = document.getElementById("mazeContainer")
    mazeContainer.innerHTML = ""//set empty.
    mazeContainer.appendChild(canvas)
}//make maze

function test_neighbors() {
    
}