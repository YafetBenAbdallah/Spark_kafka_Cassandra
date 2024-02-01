# Use a base image with Spark and Hadoop installed
FROM spark

# Set the working directory
WORKDIR /app

# Copy the Python scripts and dependencies
COPY python1_producer.py /app/
COPY python2_consumer.py /app/
COPY requirements.txt /app/
COPY spark_consumer.py /app/

USER root
# Change ownership to the spark user
RUN chown -R spark:spark /app

# Switch to the spark user


# Install Python dependencies, including PySpark
RUN pip install --user -r requirements.txt
ENV PATH $PATH:/opt/spark/bin
# Entry point to run Spark job
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0", "/app/spark_consumer.py"]
