from paho.mqtt import client as mqtt_client
import pika
import json
from datetime import datetime

if __name__ == '__main__':
    mqtt_ip = "192.168.0.102"
    mqtt_port = 1883
    topic = "CSC8112"


    # Callback function for MQTT connection
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT OK!")

        else:
            print("Failed to connect, return code %d\n", rc)


    # Callback function will be triggered
    def on_message(client, userdata, msg):

        print(f"Get message from publisher {json.loads(msg.payload)}")
        pm25_data = json.loads(msg.payload)
        # print all PM2.5 data
        print(pm25_data)
        # print PM2.5 data whose Value is greater than 50
        greater_key = []
        for key, value in pm25_data.items():
            if value > 50:
                greater_key.append(key)
                print(f"Timestamp: {key}, Value: {value}")
        for key in greater_key:
            pm25_data.pop(key)

        # Average the value every 24 hours and print it to the console
        # Initializes the dictionary to store daily data
        daily_data = {}

        # Iterate over the data and group it into daily chunks
        for key, value in pm25_data.items():
            key = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
            # Converts the timestamp to a date object, extracting only the date part(year, month, and day).
            date = key.date()
            # print(item['Timestamp'])
            if date not in daily_data:
                daily_data[date] = {'Timestamp': key, 'Value': [], 'Average': None}
            daily_data[date]['Value'].append(value)
            # print(daily_data)
        # Calculate the daily average and use the first datetime of each day as the new timestamp
        average_data = {}
        for date, day_data in daily_data.items():
            day_data['Average_Value'] = sum(day_data['Value']) / len(day_data['Value'])
            day_data['Timestamp'] = datetime(date.year, date.month, date.day)
            average_data[f"{day_data['Timestamp']}"] = day_data['Average_Value']
            # print(day_data['Timestamp'])
            # Print new time stamps and averages for each day
            average_pm25 = f"date:{day_data['Timestamp']} 24h average:{day_data['Average_Value']:.3f}"
            print(average_pm25)

        rabbitmq_ip = "192.168.0.100"
        rabbitmq_port = 5672
        # Queue name
        rabbitmq_queque = "CSC8112"
        # Connect to RabbitMQ service
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue=rabbitmq_queque)

        # Produce message
        channel.basic_publish(exchange='',
                              routing_key=rabbitmq_queque,
                              body=json.dumps(average_data))

        connection.close()


    # Create a mqtt client object
    client = mqtt_client.Client()
    # Callback function for MQTT connection
    client.on_connect = on_connect
    client.connect(mqtt_ip, mqtt_port)
    # Subscribe MQTT topic
    client.subscribe(topic)
    client.on_message = on_message
    # Start a thread to monitor message from publisher
    client.loop_forever()
