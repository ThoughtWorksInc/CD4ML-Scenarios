from csv import DictReader
from cd4ml.filenames import file_names


def stream_raw():
    filename = file_names['raw_data']
    return (dict(row) for row in DictReader(open(filename, 'r')))
