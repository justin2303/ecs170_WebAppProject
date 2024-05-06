console.log("Script loaded");

fetch("http://localhost:5000/api/test_maze_solution")
    .then(response => {
        console.log(response.json())
    })
