import asyncio
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from kafka import KafkaConsumer
import json

app = FastAPI()

# Kafka broker address
addr = os.environ['brokerIP']
bootstrap_servers = 'localhost:9092'

# Kafka topic to consume messages from
topic = 'coordinates'

# Create a Kafka consumer instance
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    group_id='coordinates-data-consumer',
    auto_offset_reset='earliest',  # Read all messages from the beginning of the topic
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),  # Deserialize the messages from JSON format
    consumer_timeout_ms=5000  # Wait for 5 seconds if there are no new messages
)

# WebSocket endpoint
@app.websocket("/gps_data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # Accept the WebSocket connection
    try:
        for message in consumer:
            # Receive message from Kafka topic
            # Check if the message doesn't indicate the end of the stream
            date = message.value.get("date")
            if date == "end":
                break # Stop the loop if it's the case
            
            # If it's not the end of the stream, send the message to the websocket
            key = message.key
            key = int(key[2:]) # Remove the "IP" part of the key
            x_pos = message.value.get("x_pos")
            y_pos = message.value.get("y_pos")
            # Reformat the message
            new_message = dict(key=key, date=date, x_pos=x_pos, y_pos=y_pos)
            print("Sending message...")
            await websocket.send_text(json.dumps(new_message))
            await asyncio.sleep(0.1)
            print(json.dumps(new_message))
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Closing consumer...")
        await websocket.close()