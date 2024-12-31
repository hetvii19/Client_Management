// Initialize Fabric.js Canvas
const canvas = new fabric.Canvas('whiteboard');

// Add save functionality
document.getElementById('save-design').addEventListener('click', () => {
    // Convert canvas to base64 PNG image
    const sketchData = canvas.toDataURL('image/png');

    // Send sketch data to the Flask backend
    const clientId = document.getElementById('whiteboard').dataset.clientId; // Get client ID from HTML
    fetch(`/whiteboard/${clientId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sketch_data: sketchData }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert('Design saved successfully!');
                window.location.href = data.redirect_url; // Redirect to the view_clients page
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch((error) => {
            console.error('Error saving design:', error);
            alert('An error occurred while saving the design.');
        });
});

// Add pencil tool functionality
document.getElementById('pencil-btn').addEventListener('click', () => {
    canvas.isDrawingMode = true; // Enable drawing mode
    canvas.freeDrawingBrush.color = 'black'; // Set default color
    canvas.freeDrawingBrush.width = 3; // Set default pencil width
});

// Add eraser tool functionality
document.getElementById('eraser-btn').addEventListener('click', () => {
    canvas.isDrawingMode = false; // Disable drawing mode
    canvas.on('mouse:down', function (event) {
        const pointer = canvas.getPointer(event.e);
        const objects = canvas.getObjects().filter((obj) => {
            return obj.containsPoint(pointer);
        });
        objects.forEach((obj) => canvas.remove(obj)); // Remove objects under the pointer
    });
});

// Add color functionality
document.querySelectorAll('.color-option').forEach((colorBtn) => {
    colorBtn.addEventListener('click', () => {
        const color = colorBtn.getAttribute('data-color'); // Get the selected color
        canvas.freeDrawingBrush.color = color; // Set drawing brush color
    });
});
