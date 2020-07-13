CREATE DATABASE cd4ml;
\c cd4ml;

CREATE TABLE raw_data (
    id VARCHAR(16) NOT NULL,
    date VARCHAR(10) NOT NULL,
    item_nbr VARCHAR(10) NOT NULL,
    unit_sales VARCHAR(20) NOT NULL,
    family VARCHAR(36) NOT NULL,
    class VARCHAR(10) NOT NULL,
    perishable VARCHAR(1) NOT NULL,
    transactions VARCHAR(10) NOT NULL,
    year VARCHAR(4) NOT NULL,
    month VARCHAR(2) NOT NULL,
    day VARCHAR(2) NOT NULL,
    dayofweek VARCHAR(10) NOT NULL,
    days_til_end_of_data VARCHAR(3) NOT NULL,
    dayoff VARCHAR(5)
);

COPY raw_data FROM '/docker-entrypoint-initdb.d/store47-2016.csv' CSV HEADER;