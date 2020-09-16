from csv import DictReader

from cd4ml.filenames import get_problem_files
import logging

logger = logging.getLogger(__name__)


def filter_func(row):
    """
    Filter function for data
    :param row: row, dictionary
    :return: True if it should be included, False if skipped
    """
    items_to_keep = {"99197", "105574", "1963838"}
    return row['item_nbr'] in items_to_keep


def stream_raw_unfiltered(problem_name):
    file_names = get_problem_files(problem_name)
    # filename_shuffled = file_names['grocery_data_shuffled']
    filename = file_names['raw_grocery_data']
    return (dict(row) for row in DictReader(open(filename, 'r')))


def stream_raw(problem_name):
    stream = stream_raw_unfiltered(problem_name)
    return (row for row in stream if filter_func(row))


def stream_data(problem_name, max_rows_to_read=None):
    # from cd4ml.problems import read_schema_file
    # from pathlib import Path
    # categorical_fields, numeric_fields = read_schema_file(Path(Path(__file__).parent, "raw_schema.json"))

    for row_num, row in enumerate(stream_raw(problem_name)):
        if max_rows_to_read and row_num == max_rows_to_read:
            logger.info('Stopped reading file after {} rows'.format(max_rows_to_read))
            break

        yield process(row)
        # yield process_orig(row)


def process(row):
    return {'date': int(row['date'].replace('-', '')),
            'item_nbr': str(row['item_nbr']),
            'id': str(row['id']),
            'year': row['year'],
            'month': row['month'],
            'day': row['day'],
            'dayofweek': row['dayofweek'],
            'days_til_end_of_data': int(row['days_til_end_of_data']),
            'dayoff': int(row['dayoff'] == 'True'),
            'class': row['class'],
            'family': row['family'],
            'unit_sales': max(0.0, float(row['unit_sales']))}


def process_orig(row_in):
    return {'item_nbr': row_in['item_nbr'],
            'unit_sales': max(0.0, float(row_in['unit_sales'])),
            'date': row_in['date'],
            'year': row_in['year'],
            'month': row_in['month'],
            'day': row_in['day'],
            'class': row_in['class'],
            'family': row_in['family'],
            'perishable': int(row_in['perishable'] == '1'),
            'dayofweek': row_in['dayofweek'],
            'days_til_end_of_data': int(row_in['days_til_end_of_data']),
            'dayoff': int(row_in['dayoff'] == 'True'),
            'transactions': 0,
            'id': row_in['id']}
