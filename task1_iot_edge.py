import json
from paho.mqtt import client as mqtt_client
from datetime import datetime
import requests

if __name__ == '__main__':
    # Callback function for MQTT connection
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT OK!")
        else:
            print("Failed to connect, return code %d\n", rc)


    # get data from Urban Observatory Platform
    url = "https://newcastle.urbanobservatory.ac.uk/api/v1.1/sensors/PER_AIRMON_MONITOR1135100/data/json/?starttime=20230601&endtime=20230831"

    # Request data from Urban Observatory Platform
    resp = requests.get(url)

    # Convert response(Json) to dictionary format
    raw_data_dict = json.loads(resp.text)
    # Create a list to store data
    pm25_data = {}
    for data in raw_data_dict["sensors"]:
        for details in data["data"]["PM2.5"]:
            timestamp = details['Timestamp']
            value = details['Value']
            timestamp = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            pm25_data[timestamp] = value
    # print(pm25_data)
    #
    mqtt_ip = "192.168.0.102"
    mqtt_port = 1883
    topic = "CSC8112"

    # Create a mqtt client object
    client = mqtt_client.Client()

    # Connect to MQTT service
    client.on_connect = on_connect
    client.connect(mqtt_ip, mqtt_port)

    # Publish message to MQTT
    # Note: MQTT payload must be a string, bytearray, int, float or None

    msg = json.dumps(pm25_data)
    client.publish(topic, msg)
