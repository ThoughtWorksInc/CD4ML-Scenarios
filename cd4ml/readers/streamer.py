from cd4ml.readers.file_reader import CSVDictionaryReader
from cd4ml.readers.postgres import PostgresReader


class DataStreamer:
    def __init__(self, data_source):
        if data_source == "file":
            self.reader = CSVDictionaryReader()

        elif data_source == "postgres":
            self.reader = PostgresReader()
        else:
            raise ValueError("data_source must be 'file' or 'postgres'")

    def stream_data(self):
        return (dict(row) for row in self.reader.stream_data())
