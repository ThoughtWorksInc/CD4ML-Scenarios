from csv import DictReader
from cd4ml.filenames import get_filenames
from cd4ml.utils import float_or_zero
from cd4ml.utils import import_relative_module

raw_schema = import_relative_module(__file__, '.', 'raw_schema').raw_schema


def stream_raw(problem_name):
    """
    :param problem_name: name of problem
    :return: stream to raw rows of house sales data
    """
    file_names = get_filenames(problem_name)
    filename = file_names['raw_house_data']
    return (dict(row) for row in DictReader(open(filename, 'r')))


def stream_data(problem_name):
    """
    :param problem_name: name of problem
    :return: stream to processed rows of house sales data
    """
    schema = raw_schema
    return (process_row(row, schema) for row in stream_raw(problem_name))


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

    row_out['price'] = max(row_out['price'], 50000)

    return row_out
