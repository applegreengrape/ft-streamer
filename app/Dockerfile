FROM python:3.8.3

WORKDIR /usr/src/app

COPY * ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install mysql-client

ENTRYPOINT ["bash", "start.sh"]