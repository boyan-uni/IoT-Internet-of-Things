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

        data_list = []  # store data before sorting by timestamp
        for method_frame, properties, body in channel.consume(queue=rabbitmq_queue, auto_ack=True):
            data_rmq = json.loads(body)
            data_list.append(data_rmq)
        # sort
        data_list.sort(key=lambda x: x['Timestamp'])
        #
        print("Collecting Daily Average PM2.5 Data:")
        for data_rmq in data_list:
            timestamp_unix = int(data_rmq['Timestamp'])/1000
            timestamp = datetime.utcfromtimestamp(timestamp_unix).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Timestamp: {timestamp}, Value: {data_rmq['Average_Value']}")

        # close connection
        channel.cancel()
        connection.close()
    except Exception as e:
        print(f"Error Message: {e}")


if __name__ == '__main__':
    collect_data_from_rabbitmq()
