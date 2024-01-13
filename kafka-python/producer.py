from datetime import datetime
import json
from kafka import KafkaProducer

def send_message(key:str, message:dict):
    # Kafka broker address
    bootstrap_servers = 'localhost:9092'

    # Kafka topic to produce messages to
    topic = 'coordinates'

    # Create a Kafka producer instance
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serialize the messages into JSON format
    )

    # Produce messages to the Kafka topic
    key_bytes = bytes(key, encoding='utf-8')

    producer.send(topic, key=key_bytes, value=message)
    print(f"Message sent: Key={key}, \nValue={message}")

    # Ensure all messages are sent
    producer.flush()

    # Close the producer
    producer.close()
    
if __name__ == "__main__":
    try:
        current_datetime = datetime.now().isoformat()  # Get the current date and time in ISO 8601 format
        msg1 = dict(date=current_datetime, msg="Hello World")
        msg2 = dict(date=current_datetime, msg="Hello World aussi parce que pourquoi pas")
        send_message("IP1", msg1)
        send_message("IP2", msg2)
    except KeyboardInterrupt:
        print("Interrupted, stopping...")