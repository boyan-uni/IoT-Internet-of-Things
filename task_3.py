import json
import pika
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from ml_engine import MLPredictor

# RabbitMQ Setup
rabbitmq_ip = "192.168.0.100"  # cloud vm ip address
rabbitmq_port = 5672
rabbitmq_queue = "rabbitmq"
rabbitmq_username = "guest"  # default username
rabbitmq_password = "guest"  # default password

# Data collection
data_collection = []

# Connect to RabbitMQ
def connect_to_rabbitmq():
    credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    return channel

# Callback function for RabbitMQ message
def on_message(channel, method, properties, body):
    try:
        data = json.loads(body)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
        print(f"Received PM2.5 data: {data}")
        if data['Average_PM25_data'] > 50:
            print(f"Outlier detected: {data}")
        else:
            data_collection.append(data)
            if len(data_collection) >= 96:  # 24H / 15Min = 96
                process_data()

    except Exception as e:
        print(f"Error processing RabbitMQ message: {e}")

# Process data
def process_data():
    global data_collection
    df = pd.DataFrame(data_collection)
    df.set_index('Timestamp', inplace=True)
    
    # Visualization
    plt.figure(figsize=(8, 4), dpi=200)
    plt.plot(df.index, df['Average_PM25_data'], color="#FF3B1D", marker='.', linestyle="-")
    plt.title("PM2.5 Data Visualization")
    plt.xlabel("DateTime")
    plt.ylabel("PM2.5 Value")

    # Save the visualization figure
    target_dir = "Your target dir path"  # Update with your desired directory path
    target_file = "Your target file name.png"  # Update with your desired file name

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    fig = plt.gcf()
    fig.savefig(os.path.join(target_dir, target_file))
    plt.show()

    # Predict using machine learning model (code not provided here)
    predicted_values = predict_pm25(df)
    print(f"Predicted PM2.5 values: {predicted_values}")

    # Reset data_collection for the next day
    data_collection = []

# Function to predict PM2.5 (not implemented here)
def predict_pm25(df):
    # Implement your machine learning model here (code not provided)
    # You can use the data in 'df' to make predictions
    # Return a list of predicted PM2.5 values
    pass

if __name__ == '__main__':
    channel = connect_to_rabbitmq()
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=on_message, auto_ack=True)

    print("Waiting for RabbitMQ messages. To exit press CTRL+C")
    channel.start_consuming()
