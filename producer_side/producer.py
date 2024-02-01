import json
from time import sleep
from kafka import KafkaProducer
import numpy as np
import matplotlib.pyplot as plt
import os

from coordinates_generation import init_pos, first_move, make_a_move

def send_messages(addr:str, producerNumber:int, pause_time:int, num_messages:int):
    # Kafka broker address
    bootstrap_servers = [addr + ':9092']
    
    # Pause time between messages
    pause_time = 1
    
    # Number of messages to send
    num_messages = 60

    # Kafka topic to produce messages to
    topic = 'coordinates'
    
    # Key of the message
    key = 'IP' + str(producerNumber)

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
    
    for i in range(num_messages):
        try:
            date, x_pos, y_pos, angle = make_a_move(date, x_pos, y_pos, angle)
            messages[date] = [x_pos, y_pos]
            message = dict(date=date, x_pos=x_pos, y_pos=y_pos)
            
            # Send the message to the topic
            producer.send(topic, key=key_bytes, value=message)
            print(f"Sent message: Key={key}, Value={message}")
            sleep(pause_time)
        except:
            print("Problem with the move")
            return messages
    
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
    IP = os.environ['brokerIP']
    producerNumber = os.environ['producerNumber']
    num_messages = os.environ['iterations']
    pause_time = os.environ['iterationGap']

    messages = send_messages(IP if IP != '' else 'localhost', int(producerNumber) if producerNumber != '' else 1, 
                             int(pause_time) if pause_time != '' else 1, int(num_messages) if num_messages != '' else 60)
    
    #view_map(messages) # To view the map with the points just produced