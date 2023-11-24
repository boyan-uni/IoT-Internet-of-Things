import requests
import json
from paho.mqtt import client as mqtt_client
from datetime import datetime


if __name__ == '__main__':

    # Callback function for MQTT connection
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT OK!")
        else:
            print("Failed to connect, return code %d\n", rc)


    # Collect raw data from Urban Observatory (IoT Layer Back up url)
    url = "https://gist.githubusercontent.com/ringosham/fbd66654dc53c40bd4581d2828acc94e/raw/d56a0fcfd27ff7ea31e2aec3765eb2c5d64adb79/uo_data.min.json"
    response = requests.get(url)
    raw_data_dict = json.loads(response.text)
    print(raw_data_dict)

    # Extract PM2.5 data
    pm25_data = {}
    for data in raw_data_dict["sensors"]:
        for items in data["data"]["PM2.5"]:
            timestamp = items['Timestamp']
            value = items['Value']
            timestamp = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            pm25_data[timestamp] = value
    print(pm25_data)

    # MQTT (Publisher)
    mqtt_ip = "192.168.0.102"  # edge vm ip address
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
