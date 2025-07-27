// Constants
const API_BASE_URL = ProcessingInstruction.env.API_BASE_URL || 'http://localhost:5000/api';
const canvas = document.getElementById('floorPlanCanvas');
const ctx = canvas.getContext('2d');
const GRID_SIZE_X = 60;
const GRID_SIZE_Y = 60;
const CELL_SIZE_X = canvas.width / GRID_SIZE_X;
const CELL_SIZE_Y = canvas.height / GRID_SIZE_Y;

let allRooms = [];
let roomBlocksData = {};

// Utility Functions
function gridToCanvas(gridCol, gridRow) {
    const canvasX = gridCol * CELL_SIZE_X + CELL_SIZE_X / 2;
    const canvasY = gridRow * CELL_SIZE_Y + CELL_SIZE_Y / 2;
    return { x: canvasX, y: canvasY };
}

function showMessage(message, type) {
    const messageBox = document.getElementById('messageBox');
    messageBox.textContent = message;
    messageBox.className = `message-box ${type}`;
    messageBox.style.display = 'block';
    setTimeout(() => {
        messageBox.style.display = 'none';
        messageBox.className = 'message-box';
    }, 5000);
}

// Floor and Room Handling
function changeFloor(floorNum) {
    const tabs = document.querySelectorAll('.floor-tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    tabs[floorNum - 1].classList.add('active');

    const roomLists = document.querySelectorAll('.room-list');
    roomLists.forEach(list => list.classList.remove('active'));
    
    if (floorNum === 1) {
        document.getElementById('floor1Rooms').classList.add('active');
        updateLocationLists(allRooms);
    } else {
        showMessage('This floor is currently under development', 'info');
        updateLocationLists([]);
    }
}

function selectRoom(roomName) {
    showMessage(`Selected room: ${roomName.replace(/\b\w/g, c => c.toUpperCase())}`, 'success');
    
    const currentLocation = document.getElementById('currentLocation');
    if (!currentLocation.value) {
        currentLocation.value = roomName.replace(/\b\w/g, c => c.toUpperCase());
    } else {
        document.getElementById('destination').value = roomName.replace(/\b\w/g, c => c.toUpperCase());
    }
}

// Datalist Management
function updateDatalistOptions(input, datalist) {
    const value = input.value.toLowerCase();
    const filteredRooms = allRooms.filter(room => 
        room.toLowerCase().includes(value)
    );
    
    datalist.innerHTML = '';
    filteredRooms.forEach(room => {
        const option = document.createElement('option');
        option.value = room.replace(/\b\w/g, c => c.toUpperCase());
        datalist.appendChild(option);
    });
}

// Map Initialization
async function initializeMap() {
    try {
        const roomsResponse = await fetch(`${API_BASE_URL}/get_rooms`);
        if (!roomsResponse.ok) throw new Error(`HTTP error! status: ${roomsResponse.status}`);
        allRooms = await roomsResponse.json();

        const currentLocationInput = document.getElementById('currentLocation');
        const destinationInput = document.getElementById('destination');
        const currentLocationList = document.getElementById('currentLocationList');
        const destinationList = document.getElementById('destinationList');

        currentLocationInput.addEventListener('input', () => 
            updateDatalistOptions(currentLocationInput, currentLocationList)
        );
        destinationInput.addEventListener('input', () => 
            updateDatalistOptions(destinationInput, destinationList)
        );

        updateDatalistOptions(currentLocationInput, currentLocationList);
        updateDatalistOptions(destinationInput, destinationList);

        const roomBlocksResponse = await fetch(`${API_BASE_URL}/get_room_blocks`);
        if (!roomBlocksResponse.ok) throw new Error(`HTTP error! status: ${roomBlocksResponse.status}`);
        roomBlocksData = await roomBlocksResponse.json();

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        showMessage('Map loaded and rooms populated successfully!', 'success');

    } catch (error) {
        console.error('Initialization Error:', error);
        showMessage(`Failed to initialize map: ${error.message}. Please check backend server.`, 'error');
    }
}

// Path Finding and Drawing
async function findAndDrawPath() {
    const currentLocation = document.getElementById('currentLocation').value.toLowerCase();
    const destination = document.getElementById('destination').value.toLowerCase();

    if (!currentLocation || !destination) {
        showMessage('Please select both a current location and a destination.', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/find_path`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                currentLocation: currentLocation,
                destination: destination
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const path = data.path;
        const startCoords = data.start_coords;
        const endCoords = data.end_coords;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (path && path.length > 0) {
            drawPath(path, startCoords, endCoords);
            showMessage(`Path found from ${currentLocation.toUpperCase()} to ${destination.toUpperCase()}.`, 'success');
        } else {
            showMessage('No path found between the selected locations.', 'error');
        }

    } catch (error) {
        console.error('Error finding path:', error);
        showMessage(`Failed to find path: ${error.message}`, 'error');
    }
}

function clearPath() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    showMessage('Path cleared.', 'success');
}

function drawPath(path, startCoords, endCoords) {
    ctx.beginPath();
    ctx.strokeStyle = '#007bff';
    ctx.lineWidth = 4;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    const startPointCanvas = gridToCanvas(path[0][1], path[0][0]);
    ctx.moveTo(startPointCanvas.x, startPointCanvas.y);

    for (let i = 1; i < path.length; i++) {
        const point = path[i];
        const canvasPoint = gridToCanvas(point[1], point[0]);
        ctx.lineTo(canvasPoint.x, canvasPoint.y);
    }
    ctx.stroke();

    // Draw start marker
    const startCanvasPos = gridToCanvas(startCoords[1], startCoords[0]);
    ctx.fillStyle = 'green';
    ctx.beginPath();
    ctx.arc(startCanvasPos.x, startCanvasPos.y, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw end marker
    const endCanvasPos = gridToCanvas(endCoords[1], endCoords[0]);
    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.arc(endCanvasPos.x, endCanvasPos.y, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 2;
    ctx.stroke();
}

// Voice Recognition
function startVoiceInput(inputId) {
    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
        showMessage('Speech recognition is not supported in your browser. Please use Chrome or Edge.', 'error');
        return;
    }

    const button = event.target;
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    
    button.classList.add('recording');
    
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 3;

    let speechDetected = false;
    let recognitionEnded = false;

    recognition.onresult = (event) => {
        if (recognitionEnded) return;
        
        speechDetected = true;
        recognitionEnded = true;
        const results = event.results[0];
        let matchFound = false;

        for (let i = 0; i < results.length && !matchFound; i++) {
            const text = results[i].transcript.toLowerCase();
            console.log(`Attempt ${i + 1} recognized text:`, text);
            
            for (const room of allRooms) {
                if (text.includes(room.toLowerCase())) {
                    document.getElementById(inputId).value = room;
                    showMessage(`Recognized: ${room}`, 'success');
                    matchFound = true;
                    break;
                }
            }
        }

        if (!matchFound) {
            showMessage(`Could not find a matching room in: "${results[0].transcript}". Please try again.`, 'error');
        }

        try {
            recognition.abort();
        } catch (e) {
            console.log('Recognition already stopped');
        }
    };

    recognition.onerror = (event) => {
        if (recognitionEnded) return;
        
        console.error('Speech recognition error:', event.error);
        if (!speechDetected && !recognitionEnded) {
            if (event.error === 'not-allowed') {
                showMessage('Microphone access denied. Please allow microphone access and try again.', 'error');
            } else if (event.error === 'no-speech' && !speechDetected) {
                showMessage('No speech was detected. Please try again.', 'error');
            }
        }
    };

    recognition.onend = () => {
        if (!recognitionEnded) {
            recognitionEnded = true;
            if (!speechDetected) {
                showMessage('No speech was detected. Please try again.', 'error');
            }
        }
        button.classList.remove('recording');
    };

    try {
        recognition.start();
        showMessage('Listening... Please speak the room name.', 'success');
    } catch (error) {
        console.error('Error starting speech recognition:', error);
        showMessage('Could not start speech recognition. Please try again.', 'error');
        button.classList.remove('recording');
    }
}

// Initialize the map when the page loads
window.onload = initializeMap;
