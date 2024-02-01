# Use the official Kafka image
FROM wurstmeister/kafka

# Add your custom configurations if needed
# COPY custom-server.properties /opt/kafka/config/server.properties

# Create a directory for scripts
WORKDIR /scripts

# Download wait-for-it.sh from GitHub
RUN curl -LJO https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Copy the create-topic.sh script into the image
COPY create-topic.sh /scripts/
RUN chmod +x create-topic.sh

# Entrypoint to run the script after Kafka starts
ENTRYPOINT ["/scripts/create-topic.sh"]
