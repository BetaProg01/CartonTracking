import json
from time import sleep
from kafka import KafkaProducer
import numpy as np
import matplotlib.pyplot as plt
import ipaddress

from coordinates_generation import init_pos, first_move, make_a_move

def send_messages(IP:str="localhost", producerNumber:int=1):
    # Kafka broker address
    bootstrap_servers = [IP + ':9092']
    
    # Pause time between messages
    pause_time = 0.05
    
    # Number of messages to send
    num_messages = 100

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

# To validate the IP address
def validate_ip(ip):
    if ip == '' or ip == 'localhost':
        return True
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# To validate the producer number
def validate_producer_number(number):
    if number == '':
        return True
    return number.isdigit() and 1 <= int(number) <= 100  # Assuming producer number should be between 1 and 100

if __name__ == "__main__":
    IP = input("Enter IP address of the kafka host (default is localhost) : ")
    while not validate_ip(IP):
        print("Invalid IP address. Please try again.")
        IP = input("Enter IP address of the kafka host (default is localhost) : ")

    producerNumber = input("Enter producer number (default is 1) : ")
    while not validate_producer_number(producerNumber):
        print("Invalid producer number. Please try again.")
        producerNumber = input("Enter producer number (default is 1) : ")

    messages = send_messages(IP if IP != '' else 'localhost', int(producerNumber) if producerNumber != '' else 1)
    
    #view_map(messages) # To view the map with the points just produced