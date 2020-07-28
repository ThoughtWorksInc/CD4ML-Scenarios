from csv import DictReader
from cd4ml.problems.groceries.config.raw_schema import raw_schema
from cd4ml.utils import float_or_zero
from cd4ml.problems.groceries.download_data.download_data import get_grocery_url_and_files


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


def stream_raw_unfiltered(pipeline_params):
    """

    :param pipeline_params: pipeline_params data structure
    :return: stream to all raw rows of grocery data
    """
    assert pipeline_params['problem_name'] == 'groceries'
    _, __, filename_shuffled = get_grocery_url_and_files(pipeline_params)
    return (dict(row) for row in DictReader(open(filename_shuffled, 'r')))


def stream_raw(pipeline_params):
    """
    :param pipeline_params: pipeline_params data structure
    :return: stream to filtered rows of grocery data
    """
    stream = stream_raw_unfiltered(pipeline_params)
    return (row for row in stream if filter_func(row))


def stream_data(pipeline_params):
    """
    :param pipeline_params: pipeline_params data structure
    :return: stream to processed rows of house sales data
    """
    schema = raw_schema
    max_rows = pipeline_params['problem_params']['max_rows_to_read']
    for row_num, row in enumerate(stream_raw(pipeline_params)):
        if max_rows and row_num == max_rows:
            print('Stopped reading file after %s rows' % max_rows)
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
