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

if __name__ == '__main__':

    try:
        # Collect data from RabbitMQ
        credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue)

        timestamps = []  # store timestamps
        values = []  # store values

        print("Collecting Daily Average PM2.5 Data:")
        for method_frame, properties, body in channel.consume(queue=rabbitmq_queue, auto_ack=True):
            data_rmq = json.loads(body)

            timestamp_unix = int(data_rmq['Timestamp']) // 1000
            timestamp = datetime.utcfromtimestamp(timestamp_unix).strftime('%d/%m')
            value = data_rmq['Average_Value']

            timestamps.append(timestamp)
            values.append(value)

            print(f"Timestamp: {timestamp}, Value: {value}")

        # close connection
        channel.cancel()
        connection.close()

        data_re = {
            'Timestamp': timestamps,
            'Value': values
        }

        # 可视化
        data_df = pd.DataFrame(data_re)
        # Initialize a canvas
        plt.figure(figsize=(8, 4), dpi=200)
        # Plot data into canvas
        plt.plot(data_df["Timestamp"], data_df["Value"], color="#FF3B1D", marker='.', linestyle="-")
        plt.title('Daily Average PM2.5 Data')
        plt.xlabel('DateTime')
        plt.ylabel('Value')
        # plt.legend()
        plt.savefig('daily_pm25.png')
        plt.show()

        # 预测
        data_df = pd.DataFrame(data_past)
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
    




# Visualize prediction results
def visualize_forecast(data_forcast):
    data_df = pd.DataFrame(data_forcast)
    
    # Initialize a canvas
    plt.figure(figsize=(8, 4), dpi=200)

    # Plot data into canvas
    plt.plot(data_df["Timestamp"], data_df["Value"], color="#FF3B1D", marker='.', linestyle="-")
    plt.title('PM2.5 Data Prediction')
    plt.xlabel('Date')
    plt.ylabel('Value')
    # plt.legend()
    plt.savefig('pm25_prediction.png')
    plt.show()



    
