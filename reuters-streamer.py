import feedparser
import os
import time
import mysql.connector
from threading import Thread

def reuters(topic, url):
    try:
        cnx = mysql.connector.connect(user='root', 
                                      password='root',
                                      host='127.0.0.1',
                                      database='news', 
                                      port=6060)
        cursor = cnx.cursor()
        q = "select title from reuters order by id desc limit 1"
        feed = feedparser.parse(url)
        for entry in feed['entries']:
            title = entry['title']
            link = entry['link']
            published = entry['published']
            cursor.execute(q)
            records = cursor.fetchall()
            if records:
                _title = records[0][0]
            else:
                print('db init')
                data_entry = ("INSERT INTO reuters "
                "(title, link, published_at, tag) "
                "VALUES (%s, %s, %s, %s)")
                value = (title, link, published, topic)
                cursor.execute(data_entry, value)
                cursor.execute(q)
                records = cursor.fetchall()
                _title = records[0][0]
            print(_title)
            if title == _title:
                print('no new news yet')
            else:
                print('add new news')
                data_entry = ("INSERT INTO reuters "
                "(title, link, published_at, tag) "
                "VALUES (%s, %s, %s, %s)")
                value = (title, link, published, topic)
                cursor.execute(data_entry, value)
        cnx.commit()
        cnx.close()    
    except Exception as e:
            print(e)

def reuters_runner(topic, url):
    while True:
        reuters(topic, url)    

urls = [
        ['news', 'https://ir.thomsonreuters.com/rss/news-releases.xml'],
        ['event', 'https://ir.thomsonreuters.com/rss/events.xml'],
        ['sec', 'https://ir.thomsonreuters.com/rss/sec-filings.xml']
    ]

for url in urls:
    print(url[0], url[1])
    t = Thread(target=reuters_runner, args=(url[0], url[1],))
    t.start()