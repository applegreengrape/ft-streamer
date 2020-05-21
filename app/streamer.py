import feedparser
import os
import time
import mysql.connector

def reuters(topic, url):
    try:
        cnx = mysql.connector.connect(user='root', 
                                      password='root',
                                      host='localhost',
                                      port = 3308, 
                                      database='news',)
        cursor = cnx.cursor()
        q = "select title from latest limit 1"
        update_latest = ("UPDATE latest SET title = %s, publisher = %s, tag = %s  WHERE id = 1")
        data_entry = ("INSERT INTO reuters "
                          "(title, link, published_at, tag) "
                          "VALUES (%s, %s, %s, %s)")
        feed = feedparser.parse(url)
        rows = []
        for entry in feed['entries']:
            title = entry['title']
            link = entry['link']
            published = entry['published']
            item=[title, link, published]
            rows.append(item)
        cursor.execute(q)
        records = cursor.fetchall()
        if records:
            new_news = []
            _title = records[0][0]
            for r in rows:
                if r[0] == _title:
                    print('duplicated news')
                else:
                    item=[title, link, published]
                    new_news.append(item)
            for n in new_news:
                value = (n[0], n[1], n[2], topic)
                cursor.execute(data_entry, value)
            cursor.execute(update_latest, (new_news[0][0], 'reuters', topic))
        else:
            print('streaming init')
            for r in rows:
                value = (r[0], r[1], r[2], topic)
                cursor.execute(data_entry, value)
            cursor.execute(update_latest, (rows[0][0], 'reuters', topic))
        cnx.commit()
        cnx.close()    
    except Exception as e:
            print(e)

def main():
    urls = [
            ['news', 'https://ir.thomsonreuters.com/rss/news-releases.xml'],
            ['event', 'https://ir.thomsonreuters.com/rss/events.xml'],
            ['sec', 'https://ir.thomsonreuters.com/rss/sec-filings.xml']
        ]

    for url in urls:
        while True:
            reuters(url[0], url[1])

while True:
    reuters('news', 'https://ir.thomsonreuters.com/rss/news-releases.xml')