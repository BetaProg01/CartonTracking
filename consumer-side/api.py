# Import FastAPI and WebSocket from the fastapi module
from fastapi import FastAPI, WebSocket

# Create a new FastAPI application
app = FastAPI()

# Define a new WebSocket route at "/gps_data"
@app.websocket("/gps_data")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()
    # Enter a loop where the server waits for a message from the client
    while True:
        # Wait for the client to send a message and store it in the variable "data"
        data = await websocket.receive_text()
        # Send a response back to the client. The response is the received message prefixed with "Message text was: "
        await websocket.send_text(f"Message text was: {data}")