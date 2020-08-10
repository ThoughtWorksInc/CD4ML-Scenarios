from csv import DictReader

from cd4ml.filenames import get_filenames
import logging

from cd4ml.utils.utils import float_or_zero

logger = logging.getLogger(__name__)

# TODO Read the appropriate schema files and assign "raw_schema"

def filter_func(row):
    """
    Filter function for data
    :param row: row, dictionary
    :return: True if it should be included, False if skipped
    """
    items_to_keep = {"99197", "105574", "1963838"}
    return row['item_nbr'] in items_to_keep


def stream_raw_unfiltered(problem_name):
    file_names = get_filenames(problem_name)
    filename_shuffled = file_names['grocery_data_shuffled']
    return (dict(row) for row in DictReader(open(filename_shuffled, 'r')))


def stream_raw(problem_name):
    stream = stream_raw_unfiltered(problem_name)
    return (row for row in stream if filter_func(row))


def stream_data(problem_name, max_rows_to_read=None):
    from cd4ml.problems import read_schema_file
    from pathlib import Path
    categorical_fields, numeric_fields = read_schema_file(Path(Path(__file__).parent, "raw_schema.json"))

    for row_num, row in enumerate(stream_raw(problem_name)):
        if max_rows_to_read and row_num == max_rows_to_read:
            logger.info('Stopped reading file after {} rows'.format(max_rows_to_read))
            break
        yield process_row(row, categorical_fields, numeric_fields)


def process_row(row, categorical_fields, numeric_fields):
    """
    Process a raw row of house data and give it the right schema
    :param row: raw row
    :param schema: raw_schema_dict
    :return: processed row
    """
    row_out = {k: row[k] for k in categorical_fields}

    for field in numeric_fields:
        row_out[field] = float_or_zero(row[field])

    return row_out
