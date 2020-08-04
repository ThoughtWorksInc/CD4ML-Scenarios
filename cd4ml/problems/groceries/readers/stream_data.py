from csv import DictReader
from cd4ml.utils import float_or_zero, import_relative_module
from cd4ml.filenames import get_filenames
raw_schema = import_relative_module(__file__, '.', 'raw_schema').raw_schema


def filter_func(row):
    """
    Filter function for data
    :param row: row, dictionary
    :return: True if it should be included, False if skipped
    """
    items_to_keep = {"99197", "105574", "1963838"}
    if row['item_nbr'] in items_to_keep:
        return True

    return False


def stream_raw_unfiltered(problem_name):
    file_names = get_filenames(problem_name)
    filename_shuffled = file_names['grocery_data_shuffled']
    return (dict(row) for row in DictReader(open(filename_shuffled, 'r')))


def stream_raw(problem_name):
    stream = stream_raw_unfiltered(problem_name)
    return (row for row in stream if filter_func(row))


def stream_data(problem_name, max_rows_to_read=None):
    schema = raw_schema
    for row_num, row in enumerate(stream_raw(problem_name)):
        if max_rows_to_read and row_num == max_rows_to_read:
            print('Stopped reading file after %s rows' % max_rows_to_read)
            break
        yield process_row(row, schema)


def process_row(row, schema):
    """
    Process a raw row of house data and give it the right schema
    :param row: raw row
    :param schema: raw_schema_dict
    :return: processed row
    """

    catergorical_fields = list(schema['categorical'])
    numeric_fields = schema['numerical']

    # Make sure there are no overlaps
    overlap = set(catergorical_fields).intersection(numeric_fields)
    assert len(overlap) == 0

    row_out = {k: row[k] for k in catergorical_fields}

    for field in numeric_fields:
        row_out[field] = float_or_zero(row[field])

    return row_out
