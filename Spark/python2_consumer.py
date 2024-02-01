from kafka import KafkaConsumer
import time

# Adding a delay to allow Kafka to initialize
time.sleep(15)

# Kafka consumer configuration
consumer = KafkaConsumer('help_topic', bootstrap_servers='kafka:9093')

# Consume messages
for message in consumer:
    message_content = message.value.decode('utf-8')
    print(f"Received message: {message_content}")

    # Add logic to handle messages as needed in python2
    # For example, you might want to perform some specific action
    # based on the content of the message
    if "help" in message_content:
        print("This is a help message.")
    else:
        print("This is a regular message.")
