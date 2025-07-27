TEAM NAME
CODE CREW

TEAM MEMBERS
Sneha Elza David
S Priscilla Angeline
Tania Sophy Jose

Project: QRGo - Intuitive Indoor Navigation

Problem:Navigating large indoor spaces (hospitals, campuses) is confusing without GPS, often relying on costly hardware (beacons) or inconvenient 
app installations.
Our Solution:QRGo provides an accurate, app-free, browser-based indoor navigation system.
How it Works:It uses a grid-based floorplan and the A* pathfinding algorithm for precise route calculation and visual guidance.
Key Benefits:Requires no GPS, Wi-Fi, Bluetooth, or expensive hardware, and is instantly accessible via a simple QR code scan.

Tech Stack (purely software based)

Languages Used: Python, JavaScript, HTML, CSS
Frameworks Used: Flask 
Libraries & Tools: NumPy, heapq, os, Flask-Cors 

Implementation Overview

- Scan a QR code at the building entrance.
- Instantly opens the web-based navigation page
- User inputs their current location and destination by room name.
- The shortest path is highlighted on the floorplan using the A* algorithm.

Detailed Workflow

Step 1: Grid-Based Floorplan
- The entire indoor map is overlaid with a coordinate grid.
- Each room is associated with a specific (row, column) pair marking the door’s location.
- A walkability matrix (1 = walkable, 0 = obstacle) is used for pathfinding.

Step 2: Room Name Mapping
- Users interact using **familiar room names (like “Reception” or “Pharmacy”).
- These names are mapped to exact grid coordinates via a JSON mapping.

Step 3: A* Pathfinding Algorithm
- The backend uses the A* algorithm to compute the shortest walkable path.
- It avoids walls and blocked paths, returning the optimal route.
- The result is visually traced on the floorplan and optionally described with voice or text instructions.


Demo Screenshots
- Webpage    : https://drive.google.com/file/d/1DX2nTTqbmqhnpydGPgLANhRDrWr6S_CD/view?usp=sharing
- Path shown : https://drive.google.com/file/d/10koyhAOBXC5hbh5RCARQlF4dH6QkcIqj/view?usp=sharing


