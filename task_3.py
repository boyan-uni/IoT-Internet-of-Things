import json
import pika

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
            print(f"Timestamp: {pm25_data['Timestamp']}, Average PM2.5: {pm25_data['Average_PM25_data']}")

        # 停止消费队列并关闭连接
        channel.cancel()
        connection.close()
    except Exception as e:
        print(f"Error collecting daily average PM2.5 data from RabbitMQ: {e}")

if __name__ == '__main__':
    collect_data_from_rabbitmq()
