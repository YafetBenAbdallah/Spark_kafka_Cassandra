#!/bin/bash

# Wait for Zookeeper to be ready
./wait-for-it.sh zookeeper:2181 -t 0

# Explicitly wait for Kafka broker to be ready
./wait-for-it.sh kafka:9093 -t 0

# Create Kafka topic
/opt/kafka/bin/kafka-topics.sh --create --topic help_topic --partitions 1 --replication-factor 1 --zookeeper zookeeper:2181
