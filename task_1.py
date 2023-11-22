import requests
import paho.mqtt.client as mqtt_client
import json

# task_1: data_injector_component



def collect_raw_data():
    # url = "http://uoweb3.ncl.ac.uk/api/v1.1/sensors/PER_AIRMON_MONITOR1135100/data/json/?starttime=20230601&endtime=20230831"
    url = "https://gist.githubusercontent.com/ringosham/fbd66654dc53c40bd4581d2828acc94e/raw/d56a0fcfd27ff7ea31e2aec3765eb2c5d64adb79/uo_data.min.json"
    resp = requests.get(url)
    raw_data_dict = resp.json()
    return raw_data_dict

def extract_pm25_data(raw_data_dict):
    pm25_data =[]
    for sensor in raw_data_dict['sensors']:
        if 'PM2.5' in sensor['data']:
            for entry in sensor['data']['PM2.5']:
                pm25_data.append({'Timestamp': entry['Timestamp'],'Value':entry['Value']})
    return pm25_data

def publish_mqtt(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status ==0:
        print(f"Sent '{msg}' to topic '{topic}")
    else:
        print(f"Failed to send message to topic '{topic}")


def main():
    mqtt_ip = "192.168.0.102"
    mqtt_port = 1883
    topic = "CSC8112"

    client = mqtt_client.Client()
    client.connect(mqtt_ip, mqtt_port)

    raw_data_dict = collect_raw_data()
    print(raw_data_dict)
    pm25_data = extract_pm25_data(raw_data_dict)
    print(pm25_data)

    for data in pm25_data:
        publish_mqtt(client, topic, json.dumps(data))

    client.disconnect()


if __name__ == '__main__':
    main()



