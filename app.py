# app.py

# 1. Import necessary modules
from flask import Flask, request, jsonify  # Flask: the main web framework; request: to get data from frontend; jsonify: to send data as JSON
from flask_cors import CORS              # Flask-CORS: handles cross-origin requests (allows your browser to talk to your server)
import os
from pathfinder import ( # Import specific functions and data from your 'pathfinder.py' file
    astar,                 # Your A* pathfinding algorithm
    get_room_coordinates,  # Function to get coordinates from a room name
    get_all_room_names,    # Function to get a list of all room names
    find_closest_room_match,  # Function to find closest matching room from speech
    HOSPITAL_GRID_DATA,    # The loaded walkability matrix (your grid)
    ROOM_BLOCKS_DATA       # The room block definitions for drawing
)

# 2. Create a Flask web application instance
app = Flask(__name__)
# `__name__` is a special Python variable that helps Flask find files and resources.

# 3. Enable CORS for your Flask app
# This line is SUPER important for development. It allows your web browser (which opens 'index.html' from your local files)
# to send requests to your Flask server (which runs at 'http://127.0.0.1:5000'). Without this, your browser would block the requests.
# For a real deployed website, you would typically make this more restrictive (e.g., only allow requests from your actual website's domain).
CORS(app)

# 4. Define your API routes (these are specific web addresses your frontend can "ask" for data)

# 4.1. Route to get all room names
# When your web browser sends a GET request to http://127.0.0.1:5000/get_rooms, this function runs.
@app.route('/get_rooms', methods=['GET'])
def get_rooms_list(): # This function name is specific to the Flask app.
    rooms = get_all_room_names() # Call the function from 'pathfinder.py' to get the list of room names
    # Convert the Python list of room names into a JSON format and send it back to the browser.
    return jsonify(rooms)

# 4.2. Route to get room block data for frontend visualization
# When your web browser sends a GET request to http://127.0.0.1:5000/get_room_blocks, this function runs.
@app.route('/get_room_blocks', methods=['GET'])
def get_room_blocks():
    # ROOM_BLOCKS_DATA is already a dictionary that's suitable for JSON.
    return jsonify(ROOM_BLOCKS_DATA)

# Speech recognition is now handled entirely in the browser using Web Speech API

# 4.4. Route to find a path between two locations
# When your web browser sends a POST request (because it's sending data) to http://127.0.0.1:5000/find_path, this function runs.
@app.route('/find_path', methods=['POST'])
def find_path():
    # Get the JSON data that the frontend sent.
    # The frontend will send a dictionary like: { "currentLocation": "reception", "destination": "general ward" }
    data = request.json
    current_location_name = data.get('currentLocation') # Safely get the value for 'currentLocation'
    destination_name = data.get('destination')           # Safely get the value for 'destination'

    # Basic check: Did the frontend actually send both location names?
    if not current_location_name or not destination_name:
        # If not, send an error message back with a 400 status code (Bad Request)
        return jsonify({"error": "Missing current location or destination in your request."}), 400

    # Get the (row, col) grid coordinates for the given room names using the helper function.
    start_coords = get_room_coordinates(current_location_name)
    end_coords = get_room_coordinates(destination_name)

    # Check if the room names provided actually exist in your 'room_coords' data.
    if not start_coords or not end_coords:
        return jsonify({"error": "Invalid room name(s) provided. Please check spelling."}), 404 # 404: Not Found

    # Validate if start/end points are actually walkable on your walkability grid.
    rows, cols = HOSPITAL_GRID_DATA.shape # Get the dimensions (e.g., 60, 60) of your walkability matrix.
    # Check if start_coords are within grid boundaries AND if the grid cell value at start_coords is 1 (walkable).
    if not (0 <= start_coords[0] < rows and 0 <= start_coords[1] < cols and HOSPITAL_GRID_DATA[start_coords[0]][start_coords[1]] == 1):
        return jsonify({"error": f"Start point '{current_location_name}' ({start_coords}) is not a walkable location on the map."}), 400
    # Do the same check for end_coords.
    if not (0 <= end_coords[0] < rows and 0 <= end_coords[1] < cols and HOSPITAL_GRID_DATA[end_coords[0]][end_coords[1]] == 1):
        return jsonify({"error": f"End point '{destination_name}' ({end_coords}) is not a walkable location on the map."}), 400

    # Call your A* pathfinding algorithm!
    # Pass the start and end coordinates, and your loaded walkability matrix (HOSPITAL_GRID_DATA).
    path = astar(start_coords, end_coords, HOSPITAL_GRID_DATA)

    # The A* algorithm returns a list of (row, col) tuples.
    # JSON prefers lists over tuples, so convert each (row, col) tuple to a [row, col] list.
    path_list_of_lists = [list(coord) for coord in path] if path else [] # If path is None, send empty list

    # Send the result back to the frontend as JSON.
    # We include the path, and also the start and end coordinates again for the frontend's convenience in drawing markers.
    return jsonify({
        "path": path_list_of_lists,
        "start_coords": list(start_coords), # Convert tuple to list for JSON
        "end_coords": list(end_coords)      # Convert tuple to list for JSON
    })

# 5. Run the Flask application
# This special Python block means the code inside it only runs when you execute 'app.py' directly (e.g., 'python app.py').
if __name__ == '__main__':
    # app.run() starts the web server.
    # debug=True: This is great for development! It automatically restarts the server when you save changes
    #             and provides detailed error messages in the browser if something goes wrong.
    #             **REMEMBER TO CHANGE debug=False FOR A REAL, DEPLOYED APPLICATION.**
    # port=5000: The server will listen on port 5000. You will access it in your browser at http://127.0.0.1:5000 (or http://localhost:5000).
    import os
    app.run(debug=os.getenv(DEBUG_VALUE), port=5000)
