import json
from time import sleep
from kafka import KafkaProducer
import numpy as np
import matplotlib.pyplot as plt

from coordinates_generation import init_pos, first_move, make_a_move

def send_messages():
    # Kafka broker address
    bootstrap_servers = 'localhost:9092'

    # Kafka topic to produce messages to
    topic = 'coordinates'
    
    # Key of the message
    key = 'IP1'

    # Create a Kafka producer instance
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serialize the messages into JSON format
    )

    # Produce messages to the Kafka topic
    key_bytes = bytes(key, encoding='utf-8')
    
    date, x_pos, y_pos = init_pos()
    messages = dict()
    messages[date] = [x_pos, y_pos]
    date, x_pos, y_pos, angle = first_move(date, x_pos, y_pos)
    
    for i in range(100):
        try:
            date, x_pos, y_pos, angle = make_a_move(date, x_pos, y_pos, angle)
            messages[date] = [x_pos, y_pos]
            message = dict(date=date, x_pos=x_pos, y_pos=y_pos)
            
            # Send the message to the topic
            producer.send(topic, key=key_bytes, value=message)
            print(f"Sent message: Key={key}, Value={message}")
            sleep(0.1)
        except:
            print("Problem with the move")
            break
    
    # Message to indicate the end of the stream
    message = dict(date="end", x_pos=-10000, y_pos=-10000)
    
    # Send the message to the topic
    producer.send(topic, key=key_bytes, value=message)
    
    # Close the producer
    producer.close()
    
    return messages

def view_map(messages:dict):
    # Load the map
    map_annoted = np.load("walkability_array.npy")
    
    # Put the points on the map
    for i, key in enumerate(messages):
        x, y = messages[key]
        if i == 0:  # If this is the first point
            plt.scatter(x, y, color='green', s=50)  # Plot the first point in green
        else:
            plt.scatter(x, y, color='red', s=5)
    
    # Plot the map
    plt.imshow(map_annoted)
    plt.show()
    
if __name__ == "__main__":
    messages = send_messages()
    
    view_map(messages)