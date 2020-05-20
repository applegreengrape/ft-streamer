### Streaming Exercise 


This repo is designed to create a small streaming application to learn more about message broker tools like RabbitMq and Apache Kafka. Then we can think about how to deploy it to multiple cloud providers (i.e. AWS, GCP, and Azure or just your on-premise datacentres).

#### How to use this repo?
- Start the message broker servers
```
// start a local kafka server 
docker-compose -f docker-compose-kafka.yaml up -d
docker-compose -f docker-compose-mq.yaml up -d
(new_env) pingzhous-MBP:ft-streamer pingzhouliu$ docker-compose -f docker-compose-kafka.yaml ps
         Name                        Command               State                         Ports                       
---------------------------------------------------------------------------------------------------------------------
ft-streamer_kafka_1       start-kafka.sh                   Up      0.0.0.0:9092->9092/tcp                            
ft-streamer_zookeeper_1   /bin/sh -c /usr/sbin/sshd  ...   Up      0.0.0.0:2181->2181/tcp, 22/tcp, 2888/tcp, 3888/tcp

(new_env) pingzhous-MBP:ft-streamer pingzhouliu$ docker-compose -f docker-compose-mq.yaml ps
         Name                       Command               State                                             Ports                                           
------------------------------------------------------------------------------------------------------------------------------------------------------------
ft-streamer_rabbitmq_1   docker-entrypoint.sh rabbi ...   Up      15671/tcp, 0.0.0.0:15672->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp
```
- Start the streamer script. Reuters news are open to public if you have FT api keys you can also kickoff the ft-streamer.py
```
pip install -r requirements.txt
python3 reuters-streamer.py
```

- Test out the streaming service
```
// kafka
python3 kafka-consumer.py

// rabbitmq 
python3 mq-consumer.py
```

docker run --name news-streamer -p 6060:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest

```python
if title == _title:
                print("no new news yet")
            else:
                data_entry = ("INSERT INTO reuters "
                "(title, link, published_at, tag) "
                "VALUES (%s, %s, %s, %s)")
                cursor.execute(data_entry, (title, link, published, topic))
```