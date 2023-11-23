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
def collect_data_from_rabbitmq():
    try:
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

            value = data_rmq['Average_Value']
            values.append(value)

            timestamp_unix = int(data_rmq['Timestamp']) / 1000
            dt_obj = datetime.fromtimestamp(timestamp_unix)
            timestamps.append(dt_obj)  # 直接添加 DateTime 对象而不是字符串

            print(f"Timestamp: {dt_obj.strftime('%Y-%m-%d %H:%M:%S')}, Value: {value}")

        # close connection
        channel.cancel()
        connection.close()

        data_res = {
            'Timestamp': timestamps,
            'Value': values
        }

        return data_res
    except Exception as e:
        print(f"Error Message: {e}")


# Visualize daily average PM2.5 data
def visualize_daily_average(data_daily):
    data_df = pd.DataFrame(data_daily)
    
    # Initialize a canvas
    plt.figure(figsize=(8, 4), dpi=200)

    # Plot data into canvas
    plt.plot(data_df["Timestamp"], data_df["Value"], color="#FF3B1D", marker='.', linestyle="-")
    plt.title('Daily Average PM2.5 Data')
    plt.xlabel('Date')
    plt.ylabel('Value')
    # plt.legend()
    plt.savefig('daily_average_pm25.png')
    plt.show()


# Predict PM2.5 using machine learning
def predict_pm25(data_past):
    # 将数据转换为DataFrame
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
    return forecast


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


if __name__ == '__main__':
    
    # Collect data from RabbitMQ
    data = collect_data_from_rabbitmq()

    # Visualize daily average PM2.5 data
    visualize_daily_average(data)

    # Predict PM2.5 using machine learning
    forecast_result = predict_pm25(data)

    # Visualize prediction results
    visualize_forecast(forecast_result)
