# Use an official Python runtime as a parent image
FROM python:3.8.10
USER root
RUN mkdir -p /usr/local/source
ADD ./task2_edge_cloud.py /usr/local/source
WORKDIR /usr/local/source

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run task_2.py whem the container lauches
CMD python3 ./task2_edge_cloud.py