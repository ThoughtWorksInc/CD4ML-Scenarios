import os
from cd4ml.readers.streamer import DataStreamer
from cd4ml.readers.postgres import PostgresReader
from cd4ml.pipeline_params import pipeline_params


def make_configuration_tuple():
    postgres_host = os.environ["POSTGRES_HOST"]
    if postgres_host is None:
        postgres_host = "127.0.0.1"
    data_settings = pipeline_params["data_reader"]

    username = data_settings["username"]
    password = data_settings["password"]
    return postgres_host, username, password


def test_read_data_raw():
    host, username, password = make_configuration_tuple()

    reader = PostgresReader(host, username, password)
    results = list(reader.read_data())
    reader.close()
    assert len(results) > 10000


def test_read_data_via_process():
    host, username, password = make_configuration_tuple()
    config_dictionary = {
            "type": "postgres",
            "host": host,
            "username": username,
            "password": password,
            "database": "cd4ml"
    }

    reader = DataStreamer(config_dictionary)
    results = list(reader.stream_data())
    reader.close()
    assert len(results) != 0
