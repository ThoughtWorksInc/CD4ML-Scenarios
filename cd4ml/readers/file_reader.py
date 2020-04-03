from csv import DictReader


class CSVDictionaryReader:
    def __init__(self, input_file):
        self.input_file = input_file

    def read_data(self):
        return (item for item in DictReader(open(self.input_file, 'r')))

    def close(self):
        pass
