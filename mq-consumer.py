import pika

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters) 
channel = connection.channel()

for method_frame, properties, body in channel.consume('news'):
    print(method_frame, properties, body)