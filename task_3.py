import json
import pika
from datetime import datetime

# RabbitMQ Setup
rabbitmq_ip = "192.168.0.100"  
rabbitmq_port = 5672
rabbitmq_queue = "rabbitmq"
rabbitmq_username = "guest"  
rabbitmq_password = "guest" 

def collect_data_from_rabbitmq():
    try:
        credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue=rabbitmq_queue)

        print("Collecting Daily PM2.5 Data:")
        for method_frame, properties, body in channel.consume(queue=rabbitmq_queue, auto_ack=True):
            pm25_data = json.loads(body)
            # print(f"Timestamp: {pm25_data['Timestamp']}, Value:{pm25_data['Average_PM25_data']}")

            timestamp_unix = pm25_data['Timestamp']
            timestamp = datetime.utcfromtimestamp(timestamp_unix).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Timestamp: {timestamp}, Value: {pm25_data['Average_PM25_data']}")

        # close connection
        channel.cancel()
        connection.close()
    except Exception as e:
        print(f"Error Message: {e}")

if __name__ == '__main__':
    collect_data_from_rabbitmq()
