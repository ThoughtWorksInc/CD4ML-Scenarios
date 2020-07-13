from cd4ml.readers.streamer import DataStreamer
from cd4ml.readers.postgres import PostgresReader
import pytest


@pytest.mark.skip('skipping postgres')
def test_read_data_raw():
    reader = PostgresReader()
    results = list(reader.stream_data())
    assert len(results) > 10000


@pytest.mark.skip('skipping postgres')
def test_read_data_via_process():
    reader = DataStreamer("postgres")
    results = list(reader.stream_data())
    assert len(results) != 0
