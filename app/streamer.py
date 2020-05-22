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
                time.sleep(1)
                print('checking')
                rows = rss(url)
                title = rows[0][0]
                if title != _title:                    
                    while title != _title:
                        for r in rows:
                            title = r[0]
                            print('new news entry')
                            if title != _title:
                                value = (r[0], r[1], r[2], topic)
                                cursor.execute(data_entry, value)
                                cnx.commit()
                            else:
                                _title = rows[0][0]
                                latest_title = rows[0][0]
                                cursor.execute(update_latest, (latest_title, 'reuters', topic))
                                cnx.commit()       
                                break                                         
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


reuters('news', 'http://feeds.reuters.com/reuters/worldnews')