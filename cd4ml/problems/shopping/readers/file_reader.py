from csv import DictReader
from cd4ml.filenames import file_names


class CSVDictionaryReader:
    def __init__(self):
        self.input_file = file_names['raw_data']

    def stream_data(self):
        return (item for item in DictReader(open(self.input_file, 'r')))
