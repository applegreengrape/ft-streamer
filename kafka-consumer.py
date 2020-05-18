from kafka import KafkaConsumer

while True:
    news_consumer = KafkaConsumer('news',
                             bootstrap_servers='localhost:9092')
    for msg in news_consumer:
        print(msg.value, msg.key)