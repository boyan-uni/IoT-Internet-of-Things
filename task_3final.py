import json
import pika
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from ml_engine import MLPredictor

# RabbitMQ Setup
rabbitmq_ip = "192.168.0.100"  
rabbitmq_port = 5672
rabbitmq_queue = "rabbitmq"
rabbitmq_username = "guest"  
rabbitmq_password = "guest" 


# Collect data from RabbitMQ
def main():
    try:
        credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue)

        timestamps = []  # store timestamps
        values = []      # store values

        print("Collecting Daily Average PM2.5 Data:")
        for method_frame, properties, body in channel.consume(queue=rabbitmq_queue, auto_ack=True):
            data_rmq = json.loads(body)

            value = data_rmq['Average_Value']
            timestamp_unix = int(data_rmq['Timestamp']) // 1000
            dt_obj = datetime.fromtimestamp(timestamp_unix)
            timestamp = dt_obj.strftime('%Y-%m-%d 00:00:00')
            timestamps.append(timestamp)
            values.append(value)

            print(f"Timestamp: {timestamp}, Value: {value}")

        data = {
            'Timestamp': timestamps,
            'Value': values
        }

        # close connection
        channel.cancel()
        connection.close()

        data_df = pd.DataFrame(data)
    
        # Initialize a canvas
        plt.figure(figsize=(8, 4), dpi=200)

        # Plot data into canvas
        plt.plot(data_df["Timestamp"], data_df["Value"], color="#FF3B1D", marker='.', linestyle="-")
        plt.title('Daily Average PM2.5 Data')
        plt.xlabel('DateTime')
        plt.ylabel('Value')
        plt.savefig('figure1.png')
        # plt.show()

        # Format Timestamp to %Y-%m-%d e.g:"2020-09-01"
        formatted_Timestamp = [timestamp.strftime('%Y-%m-%d') for timestamp in timestamps]

        # Prepare data
        data = {
            'Timestamp': formatted_Timestamp,
            'Value': values
        }
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

    except Exception as e:
        print(f"Error Message: {e}")


if __name__ == '__main__':
    main()
