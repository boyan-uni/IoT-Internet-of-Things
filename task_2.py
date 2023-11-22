import json
import pika
import pandas as pd
from paho.mqtt import client as mqtt_client

# data collection
data_collection = []


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Successfully.")
        client.subscribe(topic)
    else:
        print("Failed Connected to MQTT")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        data['Timestamp'] = str(data['Timestamp'])

        print(f"Received PM2.5 data: {data}")  # print PM2.5 data collected
        if data['Value'] > 50:
            print(f"Outlier detected: {data}")  # print data > 50
        else:
            data_collection.append(data)
            if len(data_collection) >= 96:  # 24H / 15Min = 96
                calculate_daily_average()
    except Exception as e:
        print(f"Error processing MQTT message: {e}")


def calculate_daily_average():
    global data_collection
    df = pd.DataFrame(data_collection)
    average_value = df['Value'].mean()
    timestamp = df['Timestamp'].iloc[0]
    print(f"Daily average PM2.5 for {timestamp}: {average_value}")  # print daily average value
    send_to_rabbitmq({'Timestamp': timestamp, 'Average_Value': average_value})
    data_collection = []  # clear data_collection for next day


def send_to_rabbitmq(message):
    credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=rabbitmq_queue)
    body = json.dumps(message).encode('utf-8')
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=body)
    connection.close()


if __name__ == '__main__':
    # MQTT Setup
    mqtt_ip = "192.168.0.102"  # edge vm ip address
    mqtt_port = 1883
    mqtt_username = "admin"
    mqtt_password = "public"
    topic = "CSC8112"

    # RabbitMQ Setup
    rabbitmq_ip = "192.168.0.100"  # cloud vm ip address
    rabbitmq_port = 5672
    rabbitmq_queue = "rabbitmq"
    rabbitmq_username = "guest"  # default username
    rabbitmq_password = "guest"  # default password

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=mqtt_username, password=mqtt_password)

    client.connect(mqtt_ip, mqtt_port)
    client.loop_forever()
