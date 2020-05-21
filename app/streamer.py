import feedparser
import os
import time
import mysql.connector

def rss(url):
    rows = []
    feed = feedparser.parse(url)
    for entry in feed['entries']:
        title = entry['title']
        link = entry['link']
        published = entry['published']
        item=[title, link, published]
        rows.append(item)
    return rows

def reuters(topic, url):
    try:
        cnx = mysql.connector.connect(user='root', 
                                      password='root',
                                      host='localhost',
                                      port = 3308, 
                                      database='news',)
        cursor = cnx.cursor()
        q = "select title from latest order by id desc limit 1"
        update_latest = ("INSERT INTO latest "
                      "(title, publisher, tag) "
                      "VALUES (%s, %s, %s)")
        data_entry = ("INSERT INTO reuters "
                      "(title, link, published_at, tag) "
                      "VALUES (%s, %s, %s, %s)")
        cursor.execute(q)
        records = cursor.fetchall()
        if records:
            _title = records[0][0]
            rows = rss(url)
            title = rows[0][0]
            print('init title: ', _title, title)
            while title == _title:
                print('duplicated news')
                rows = rss(url)
                title = rows[0][0]
                if title != _title:
                    print('new news')
                    while title != _title:
                        rows = rss(url)
                        for r in rows:
                            title = r[0]
                            print(title)
                            if title == _title:
                                _title = rows[0][0]
                                             
        else:
            print('streaming init')
            init_rows = rss(url)
            for r in init_rows:
                value = (r[0], r[1], r[2], topic)
                cursor.execute(data_entry, value)
                cnx.commit()
            latest_title = init_rows[0][0]
            cursor.execute(update_latest, (latest_title, 'reuters', topic))
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


reuters('news', 'https://ir.thomsonreuters.com/rss/news-releases.xml')