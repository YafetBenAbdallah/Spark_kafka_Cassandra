from kafka import KafkaProducer
import time

# Adding a delay to allow Kafka to initialize
time.sleep(10)

producer = KafkaProducer(bootstrap_servers='kafka:9093')

# Simulating sending a message with content "help"
producer.send('help_topic', value='This is a help message')

# Simulating sending a message without content "help"
producer.send('help_topic', value='This is a regular message')

# Close the producer
producer.close()
