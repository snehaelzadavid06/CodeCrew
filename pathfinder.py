# pathfinder.py

# Import necessary libraries
from heapq import heappush, heappop # For the A* priority queue
import numpy as np # For numerical operations, especially loading the matrix
import os # For handling file paths

# --- YOUR ORIGINAL ROOM COORDINATES ---
# These map room names (in lowercase) to their corresponding (row, col) grid coordinates.
# (row, col) means (Y, X) on the grid.
room_coords = {
    "waiting room": (40, 24),
    "nurse duty": (45, 40),
    "lady doctor room": (49, 38),
    "pharmacy": (49, 36), # THIS IS THE COORDINATE WE NEED TO CHECK
    "drinking water": (21, 39),
    "entrance": (41, 14),
    "homeo room": (30, 22),
    "medical officers room": (30, 29),
    "registration room": (27, 34),
    "reception": (39, 28), # Using your older reception coordinate
    "pathology lab": (41, 36),
    "washroom1": (27, 35),
    "washroom2": (29, 35),
    "labour room": (47, 44),
    "gynaecologist specialist": (47, 46),
    "recovery room": (48, 45),
    "dressing": (37, 40),
    "general ward": (37, 45),
    "ramp": (46, 17)
}

# --- YOUR ORIGINAL ROOM BLOCKS (for frontend drawing) ---
# This dictionary defines rectangular areas for each room.
# (row_start, col_start, height, width) in grid units.
room_blocks = {
    "reception": (36, 29, 4, 3),
    "waiting room": (40, 21, 12, 7),
    "pharmacy": (46, 28, 6, 7),
    "lady doctor\n room": (44, 35, 8, 4),
    "pathology lab": (40, 28, 6, 7),
    "general ward": (28, 45, 10, 7),
    "labour room": (38, 42, 8, 10),
    "recovery room": (49, 42, 3, 4),
    "washroom1": (23, 35, 4, 6),
    "washroom2": (29, 35, 3, 8),
    "homeo\n room": (23, 22, 5, 3),
    "medical\nofficers\nroom": (23, 25, 5, 3),
    "registration\n room": (23, 28, 5, 5),
    "nurse \nduty": (39, 35, 3, 4),
    "dressing": (33, 35, 5, 5),
    "gynaecologist\n specialist": (46, 46, 6, 6),
    "ramp": (48, 13,4,8),
    "entrance": (39, 10,5,4),
    "drinking \nwater": (19, 39,4,3),
}

# --- Load the walkability matrix ---
# IMPORTANT: 'walkability_matrix (3).csv' MUST be in the same directory as this pathfinder.py
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    walkability_matrix_path = os.path.join(current_dir, 'walkability_matrix (3).csv')
    walkability = np.loadtxt(walkability_matrix_path, delimiter=',')
    walkability = walkability.astype(int)
    print("Walkability matrix loaded successfully by pathfinder.py.")
except FileNotFoundError:
    print(f"Error: 'walkability_matrix (3).csv' not found at {walkability_matrix_path}.")
    print("Please ensure the CSV file is in the same directory as pathfinder.py.")
    walkability = np.ones((60, 60), dtype=int) # Fallback to all walkable
    print("Using a dummy 60x60 all-walkable grid for now.")
except Exception as e:
    print(f"An unexpected error occurred while loading walkability matrix: {e}")
    walkability = np.ones((60, 60), dtype=int)
    print("Using a dummy 60x60 all-walkable grid for now.")

# --- A* Helper Functions ---
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, end, grid):
    rows, cols = grid.shape
    open_set = []
    heappush(open_set, (heuristic(start, end), 0, start, [start]))
    visited = set()

    while open_set:
        _, cost, current, path = heappop(open_set)
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = current[0]+dr, current[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                neighbor = (nr, nc)
                if neighbor not in visited:
                    new_cost = cost + 1
                    priority = new_cost + heuristic(neighbor, end)
                    heappush(open_set, (priority, new_cost, neighbor, path + [neighbor]))
    return None # Return None if no path found

# --- Helper functions for Flask app ---
def get_room_coordinates(room_name):
    return room_coords.get(room_name.lower())

def get_all_room_names():
    return list(room_coords.keys())

def find_closest_room_match(input_text):
    """
    Find the closest matching room name for the given input text.
    Returns None if no close match is found.
    """
    input_text = input_text.lower().strip()
    
    # Direct match
    if input_text in room_coords:
        return input_text
    
    # Check if input is contained within any room name
    for room_name in room_coords:
        if input_text in room_name or room_name in input_text:
            return room_name
    
    # If no match found
    return None

# --- Variables to be exposed for import by app.py ---
HOSPITAL_GRID_DATA = walkability
ROOM_BLOCKS_DATA = room_blocks