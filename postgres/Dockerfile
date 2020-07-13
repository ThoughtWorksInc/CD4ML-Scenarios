FROM postgres:12.2
RUN apt-get update && apt-get install -y wget && \
    mkdir -p /docker-entrypoint-initdb.d && \
    wget https://storage.googleapis.com/continuous-intelligence/store47-2016.csv -O /docker-entrypoint-initdb.d/store47-2016.csv

COPY initialize.sql /docker-entrypoint-initdb.d/initialize.sql
