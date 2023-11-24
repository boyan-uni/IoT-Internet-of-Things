import pika

# Connection Successful

rabbitmq_ip = "192.168.0.100" # cloud vm ip address
rabbitmq_port = 5672
rabbitmq_queue = "rabbitmq"

# No need to set default username and password
parameters = pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, socket_timeout=60)
try:
    connection = pika.BlockingConnection(parameters)
    print("Connection Successful")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")