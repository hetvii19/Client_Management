// Ensure client_id is available from the server-side template
const clientId = "{{ client_id }}"; // Ensure that client_id is injected properly by the template engine

const canvas = document.getElementById("whiteboard");
const ctx = canvas.getContext("2d");
let isDrawing = false;
let isErasing = false;  // Track eraser mode
let currentColor = "black"; // Default color

// Event listeners for drawing on the canvas
canvas.addEventListener("mousedown", () => (isDrawing = true));
canvas.addEventListener("mouseup", () => (isDrawing = false));
canvas.addEventListener("mousemove", draw);

// Drawing function
function draw(event) {
    if (!isDrawing) return;

    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    ctx.strokeStyle = isErasing ? "white" : currentColor; // Erase with white, else draw with selected color

    ctx.lineTo(event.offsetX, event.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.offsetX, event.offsetY);
}

// Save sketch as data URL when the save button is clicked
document.getElementById("save-sketch").addEventListener("click", () => {
    const dataURL = canvas.toDataURL(); // Get the base64 image data

    // Check if clientId is available
    if (!clientId) {
        alert("Client ID is not available.");
        return;
    }

    // Sending POST request to Flask endpoint
    fetch(`/whiteboard/${clientId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sketch_data: dataURL // Send the base64 image data in JSON format
        })
    })

    .then(response => response.json()) // Handle the server's response
    .then(data => {
        if (data.success) {
            alert("Sketch saved successfully!");
            // Redirect to the home page after saving
            window.location.href = "/"; // Direct the user to the home page
        } else {
            alert("Failed to save sketch.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while saving the sketch.");
    });
});

// Toggle eraser mode when the eraser button is clicked
document.getElementById("eraser-btn").addEventListener("click", () => {
    isErasing = !isErasing; // Toggle eraser state
});

// Set pencil mode
document.getElementById("pencil-btn").addEventListener("click", () => {
    isErasing = false; // Turn off eraser mode
});

// Set selected color when a color is clicked
document.querySelectorAll(".color-option").forEach((colorOption) => {
    colorOption.addEventListener("click", () => {
        currentColor = colorOption.getAttribute("data-color"); // Set the color to the selected one
    });
});
