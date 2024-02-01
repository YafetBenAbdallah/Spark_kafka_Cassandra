from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import time
from kafka.errors import KafkaError
from kafka import KafkaConsumer

# Function to check Kafka readiness
def is_kafka_ready(bootstrap_servers, max_retries=30, retry_interval=5):
    current_retry = 0
    while current_retry < max_retries:
        try:
            # Try to create a Kafka consumer and fetch metadata
            consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id=None)
            metadata = consumer.list_topics()
            consumer.close()

            # Break the loop if successful
            return True

        except KafkaError as ke:
            print(f"Kafka connection attempt failed. Retrying in {retry_interval} seconds. Error: {str(ke)}")
            current_retry += 1
            time.sleep(retry_interval)

    return False

# Adding a dynamic delay to allow Kafka to initialize
kafka_bootstrap_servers = "kafka:9093"
if not is_kafka_ready(kafka_bootstrap_servers):
    raise Exception("Max retries reached. Unable to connect to Kafka.")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkCassandraIntegration") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .getOrCreate()

# Kafka configurations
kafka_topic = "help_topic"

# Read from Kafka topic using structured streaming
kafka_stream_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "earliest") \
    .load()

# Convert the message value to a string
processed_stream_df = kafka_stream_df \
    .selectExpr("CAST(value AS STRING) as message_content")

# Check if the message content contains "help"
help_messages_df = processed_stream_df.filter(expr("message_content = 'help'"))

# Write processed messages to Cassandra
cassandra_options = {
    "table": "messages",
    "keyspace": "my_keyspace",
    "spark.cassandra.connection.host": "cassandra"
}

query = help_messages_df \
    .writeStream \
    .foreachBatch(lambda df, epoch_id: df.write.format("org.apache.spark.sql.cassandra").mode("append").options(**cassandra_options).save()) \
    .start()

# Await termination
query.awaitTermination()
