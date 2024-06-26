# Use an official Python runtime as a parent image
FROM python:3.10

# Upgrade pip
RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.txt file to the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set the RABBITMQ_HOST, INPUT_TOPIC, FINAL_TOPIC, RABBITMQ_MAX_RETRIES (*3 sec), SERVICE_NAME, MESSAGING_SYSTEM, and KAFKA_BOOTSTRAP_SERVERS environment variables
ENV RABBITMQ_HOST=rabbitmq-service \
    INPUT_TOPIC=input_topic \
    FINAL_TOPIC=final_topic \
    RABBITMQ_MAX_RETRIES=150 \
    SERVICE_NAME=default_service \
    MESSAGING_SYSTEM=rabbitmq \
    KAFKA_BOOTSTRAP_SERVERS=kafka-service:9092

# Run uvicorn when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
