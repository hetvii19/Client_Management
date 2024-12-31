from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import base64
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# File paths
DESIGNS_DIR = "static/designs"
# Set the directory to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ensure the designs directory exists
os.makedirs(DESIGNS_DIR, exist_ok=True)

# Local data storage
client_id_counter = 1  # Simulate auto-incrementing IDs

# Function to load clients from the .txt file
def load_clients():
    try:
        with open('clients.txt', 'r') as file:
            clients = json.load(file)
    except FileNotFoundError:
        clients = []  # If the file does not exist, return an empty list
    return clients

# Function to save clients to the .txt file
def save_clients(clients):
    with open('clients.txt', 'w') as file:
        json.dump(clients, file, indent=4)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/add-client', methods=['GET', 'POST'])
def add_client():
    global client_id_counter
    clients = load_clients()  # Load existing clients from the file

    if request.method == "POST":
        # Prepare client data from the form
        client = {
            "id": client_id_counter,
            "name": request.form["name"],
            "contact": request.form["contact"],
            "address": request.form["address"],
            "delivery_date": request.form["delivery_date"],
            "design_picture": None,
            "neck": request.form.get("neck"),
            "shoulder": request.form.get("shoulder"),
            "chest": request.form.get("chest"),
            "waist": request.form.get("waist"),
            "hip": request.form.get("hip"),
            "sleeve_length": request.form.get("sleeve_length"),
            "inseam": request.form.get("inseam"),
            "thigh": request.form.get("thigh"),
            "calf": request.form.get("calf"),
            "pant_length": request.form.get("pant_length"),
            "height": request.form.get("height"),
            "torso_length": request.form.get("torso_length"),
            "sketch_url": None  # Assuming the sketch URL is added later
        }

        # Handle file upload if provided
        design_picture = request.files.get('design_picture')
        if design_picture and allowed_file(design_picture.filename):
            filename = secure_filename(design_picture.filename)
            design_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            client['design_picture'] = f"uploads/{filename}"  # Store the relative path

        # Add client to the list and increment the client_id_counter
        clients.append(client)
        client_id_counter += 1

        # Save the updated client list back to the file
        save_clients(clients)

        # Redirect to the whiteboard
        return redirect(url_for('whiteboard', client_id=client["id"]))

    # On GET request, just render the template
    return render_template('add_client.html')

@app.route('/view-clients', methods=['GET'])
def view_clients():
    # Load clients
    clients = load_clients()  # Replace with the actual function that loads client data

    # Get the search term from the request
    search_query = request.args.get('search', '').lower()

    # Filter clients based on the search query
    if search_query:
        clients = [client for client in clients if search_query in client['name'].lower() or search_query in client['contact'].lower() or search_query in client['address'].lower()]

    return render_template('view_clients.html', clients=clients)



@app.route('/client_details/<int:client_id>', methods=['GET'])
def client_details(client_id):
    # Load the clients from file
    clients = load_clients()  # Replace this with the appropriate function

    # Find the client by ID
    client = next((c for c in clients if c["id"] == client_id), None)

    if not client:
        return "Client not found", 404

    return render_template('client_details.html', client=client, client_id=client_id)


@app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    # Load the clients from file
    clients = load_clients()  # Replace this with the appropriate function

    # Find the client by ID
    client = next((c for c in clients if c["id"] == client_id), None)

    if not client:
        return "Client not found", 404

    if request.method == 'POST':
        # Update the client details
        client['name'] = request.form['name']
        client['contact'] = request.form['contact']
        client['address'] = request.form['address']
        client['delivery_date'] = request.form.get('delivery_date')

        # Update measurements
        client['measurements'] = {
            "neck": request.form.get("neck"),
            "shoulder": request.form.get("shoulder"),
            "chest": request.form.get("chest"),
            "waist": request.form.get("waist"),
            "hip": request.form.get("hip"),
            "sleeve_length": request.form.get("sleeve_length"),
            "inseam": request.form.get("inseam"),
            "thigh": request.form.get("thigh"),
            "calf": request.form.get("calf"),
            "pant_length": request.form.get("pant_length"),
            "height": request.form.get("height"),
            "torso_length": request.form.get("torso_length")
        }

        # Save the updated client data
        save_clients(clients)  # Replace this with the appropriate function

        return redirect(url_for('view_clients'))

    return render_template('edit_client.html', client=client)

@app.route("/whiteboard/<int:client_id>", methods=["GET", "POST"])
def whiteboard(client_id):
    clients = load_clients()  # Load existing clients from the file
    client = next((c for c in clients if c["id"] == client_id), None)
    if not client:
        return "Client not found", 404

    if request.method == "POST":
        try:
            # Decode the base64 image data
            sketch_data = request.json["sketch_data"]
            image_data = base64.b64decode(sketch_data.split(",")[1])

            # Save the image
            design_file_path = os.path.join(DESIGNS_DIR, f"client_{client_id}_design.png")
            with open(design_file_path, "wb") as f:
                f.write(image_data)

            # Update client's sketch URL in local storage
            client["sketch_url"] = f"designs/client_{client_id}_design.png"

            # Save the updated client list back to the file
            save_clients(clients)

            return jsonify(success=True, redirect_url=url_for('home'))

        except Exception as e:
            return jsonify(success=False, message=str(e))

    return render_template('whiteboard.html', client_id=client_id, client=client)

if __name__ == "__main__":
    app.run(debug=True)
