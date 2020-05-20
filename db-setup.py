from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'news'

TABLES = {}

TABLES['reuters'] = (
    "CREATE TABLE `reuters` ("
    "  `id` bigint auto_increment,"
    "  `title` varchar(512) DEFAULT NULL,"
    "  `link` varchar(1024) DEFAULT NULL,"
    "  `published_at` varchar(256) DEFAULT NULL,"
    "  `tag` varchar(256) DEFAULT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['ft'] = (
    "CREATE TABLE `ft` ("
   "  `id` bigint auto_increment,"
    "  `title` varchar(512) DEFAULT NULL,"
    "  `link` varchar(1024) DEFAULT NULL,"
    "  `published_at` varchar(256) DEFAULT NULL,"
    "  `tag` varchar(256) DEFAULT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1', port=6060)
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
