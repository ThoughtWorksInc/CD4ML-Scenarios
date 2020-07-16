from csv import DictReader
from cd4ml.filenames import file_names


def get_zip_lookup():
    filename = file_names['house_data_zip_lookup']
    stream = DictReader(open(filename, 'r'))
    return {row['zipcode']: row for row in stream}
