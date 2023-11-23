import pika
import json
import pandas as pd
import matplotlib.pyplot as plt
from ml_engine import MLPredictor
from datetime import datetime

if __name__ == '__main__':

    rabbitmq_ip = "192.168.0.100"  
    rabbitmq_port = 5672
    rabbitmq_queue = "rabbitmq"
    rabbitmq_username = "guest"  
    rabbitmq_password = "guest"


    def callback(ch, method, properties, body):
        print(f"Collect message from rabbitmq: {json.loads(body)}")
        average_data = json.loads(body)
        
        Timestamp = []
        Value = []
        for key, value in average_data.items():
            # 1. value: 'Value'
            average_value = int(value)
            Value.append(average_value)
            # 2. key: 'Timestamp' collected: str unix timestamp format
            timestamp_unix = int(average_data['Timestamp']) // 1000
            dt_obj = datetime.fromtimestamp(timestamp_unix)
            timestamp = dt_obj.strftime('%Y-%m-%d 00:00:00')
            Timestamp.append(timestamp)
            #
            #unix_timestamp_str = key
            #unix_timestamp = int(unix_timestamp_str)
            #datetime_str = datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            #Timestamp.append(datetime_str)
            #print(f"Timestamp: {datetime_str}, Value: {average_value}")

        # 待处理的数据
        data = {
            'Timestamp': Timestamp,
            'Value': Value
        }
        
        # 可视化
        data_df = pd.DataFrame(data)
        # Initialize a canvas
        plt.figure(figsize=(25, 10), dpi=300)
        # Plot data into canvas
        plt.plot(data["Timestamp"], data["Value"], color="#FF3B1D", marker='.', linestyle="-")
        plt.title("Averaged PM2.5 sensor data in months")
        plt.xlabel("DateTime")
        plt.ylabel("Average Value")
        # Rotate the scale label to display vertically
        plt.xticks(Timestamp, rotation='vertical')
        # Save as file
        plt.savefig("figure1.png")
        # Directly display
        plt.show()

        # Format Timestamp to %Y-%m-%d e.g:"2020-09-01"
        formatted_Timestamp = [timestamp.strftime('%Y-%m-%d') for timestamp in Timestamp]
        print(formatted_Timestamp)

        # Prepare data
        data = {
           'Timestamp': formatted_Timestamp,
           'Value': Value
        }
        
        # 机器学习引擎
        data_df = pd.DataFrame(data)

        # Create ML engine predictor object
        predictor = MLPredictor(data_df)
        # Train ML model
        predictor.train()
        # Do prediction
        forecast = predictor.predict()

        # Get canvas
        fig = predictor.plot_result(forecast)
        fig.savefig("prediction.png")
        fig.show()


    # Connect to RabbitMQ service
    credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()
    # Declare a queue
    channel.queue_declare(queue=rabbitmq_queue)

    channel.basic_consume(queue=rabbitmq_queue,
                          auto_ack=True,
                          on_message_callback=callback)

    channel.start_consuming()
