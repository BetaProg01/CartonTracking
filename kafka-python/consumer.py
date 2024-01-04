import json
from kafka import KafkaConsumer

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to consume messages from
topic = 'test'

# Create a Kafka consumer instance
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    group_id='coordinates-data-consumer',
    auto_offset_reset='earliest',  # Read all messages from the beginning of the topic
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),  # Deserialize the messages from JSON format
)

# Consume messages from the Kafka topic
try:
    for message in consumer:
        # Process the received message
        key = message.key
        value = message.value  # Get the value from the message
        print(f"Received message: Key={key}, \nValue={value}")

except KeyboardInterrupt:
    print("Closing consumer...")
finally:
    # Close the consumer
    consumer.close()