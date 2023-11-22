# FROM ubuntu:latest
# LABEL authors="student"
# ENTRYPOINT ["top", "-b"]

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container ar /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set Environmental Variables
ENV MQTT_IP = 192.168.0.102
ENV MQTT_PORT = 1883
ENV MQTT_USERNAME = admin
ENV MQTT_PASSWORD = public
ENV RABBITMQ_IP = 192.168.0.100
ENV RABBITMQ_PORT = 5672
ENV RABBITMQ_QUEUE = rabbitmq
ENV RABBITMQ_USERNAME = guest
ENV RABBITMQ_PASSWORD = guest

# Run task_2.py whem the container lauches
CMD ["python","./task_2.py"]