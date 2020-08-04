from csv import DictReader
from cd4ml.filenames import get_filenames


def get_zip_lookup(problem_name):
    file_names = get_filenames(problem_name)
    filename = file_names['house_data_zip_lookup']
    stream = DictReader(open(filename, 'r'))
    return {row['zipcode']: row for row in stream}
