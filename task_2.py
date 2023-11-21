import json
import paho.mqtt.client as mqtt
import pika
from datetime import datetime
import numpy as np

# MQTT setup
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))
    client.subscribe("CSC8112_PM25") # MQTT topic for PM2.5 data

def on_message(client, userdata, msg):
    data = json.load(msg.payload)
    process_data(data)

# RabbitMQ setup
rabbitmq_ip = "0.0.0.0"     # host
rabbitmq_port = 15672       # port
rabbitmq_queue = "rabbitmq" # queue name

# Data processing
pm25_data = {}

def process_data(data):
    Timestamp = datetime.fromtimestamp(data['Timestamp']/1000)
    date_key = Timestamp.date()
    Value = data['Value']

    # Filter outliers
    if Value>50:
        print(f"Outlier detected:{Value} at {Timestamp}")

    # Store data for averaging
    if date_key not in pm25_data:
        pm25_data[date_key] = []
    pm25_data[date_key].append(Value)

    # Calculate daily average at the end of each day
    if Timestamp.time() == datetime.min.time():
        average = np.mean(pm25_data[date_key])
        print(f"Average PM2.5 for {date_key}: {average}")
        send_to_rabbitmq(date_key, average)

def send_to_rabbitmq(date, average,channel):
    message = json.dumps({'date':str(date), 'average_pm25': average})
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue,body=message)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, socket_timeout=60))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("0.0.0.0", 1883, 60) # EMQX server address and port

    mqtt_client.loop_start()

    try:
        while True:
            pass # Keep the script running
    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        connection.close()

if __name__ == '__main__':
    main()