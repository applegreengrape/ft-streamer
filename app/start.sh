#!/bin/sh
# wait-for-postgres.sh

set -e

db_url='127.0.0.1'
db_port=3308
db_username='root'
db_password='root'

until mysql -h $db_url -u $db_username --password=$db_password -P $db_port -e "exit"; do
  >&2 echo "mysql is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "mysql is up - executing command"
python3 init_db.py &
wait
python3 streamer.py &