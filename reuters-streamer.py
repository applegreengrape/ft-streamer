# https://ir.thomsonreuters.com/rss-feeds

import feedparser
import os
import time
import threading
from threading import Thread
import pika
from kafka import KafkaProducer

class rss_parser:
    def __init__(req, url):
        req.url = url
    
    def fetchDetails(req):
        try:
            url = req.url
            title = ''
            link = ''
            row = ''
            result = []
            feed = feedparser.parse(url)
            for entry in feed['entries']:
                title = entry['title']
                link = entry['link']
                published = entry['published']
                row = [title, link, published]
                result.append(row)
            return result
        except Exception as e:
            print(e)

def getstats(url):
    try:
        rss = rss_parser(url)
        result = rss.fetchDetails()
        return result      
    except Exception as e:
            print(e)

def rabbitmq(topic, message):
    credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
    parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
    connection = pika.BlockingConnection(parameters) #default is localhost
    channel = connection.channel() 
    channel.queue_declare(queue=topic) 
    channel.basic_publish(exchange='', routing_key=topic, body=message)

def kafka(topic, message):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    msg = bytes(message, encoding='utf-8')
    producer.send(topic, key=msg, value=msg)

def worker(topic, url):
    try:
        result = getstats(url)
        title_init = result[0][0]
        latest_title = result[0][0]
        while latest_title == title_init :
            result = getstats(url)
            latest_title = result[0][0]
            for r in result:
                msg = '{0}, {1}, {2}'.format(r[0], r[1], r[2])
                rabbitmq(topic, msg)
                kafka(topic, msg)
                print(msg)

            if latest_title != title_init:
                result = getstats(url)
                latest_title = result[0][0]
                title_init = result[0][0]
                for r in result:
                    msg = '{0}, {1}, {2}'.format(r[0], r[1], r[2])
                    rabbitmq(topic, msg)
                    kafka(topic, msg)
                    print(msg)
            else:
                continue
    except Exception as e:
            print(e)
    
urls = [
        ['news', 'https://ir.thomsonreuters.com/rss/news-releases.xml'],
        ['event', 'https://ir.thomsonreuters.com/rss/events.xml'],
        ['sec', 'https://ir.thomsonreuters.com/rss/sec-filings.xml']
    ]

for url in urls:
    print(url[0], url[1])
    t = Thread(target=worker, args=(url[0], url[1],))
    t.start()