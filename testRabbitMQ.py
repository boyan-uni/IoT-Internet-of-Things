import pika

# Connection Successful

rabbitmq_ip = "192.168.0.100" # cloud vm ip address
rabbitmq_port = 5672
rabbitmq_queue = "rabbitmq"
rabbitmq_username = "guest"  # default username
rabbitmq_password = "guest"  # default password

credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
parameters = pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, credentials=credentials)

try:
    connection = pika.BlockingConnection(parameters)
    print("Connection Successful")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")