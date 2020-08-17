from csv import DictReader
from cd4ml.filenames import get_filenames
from cd4ml.utils.utils import float_or_zero


def stream_raw(problem_name):
    """
    :param problem_name: name of problem
    :return: stream to raw rows of house sales data
    """
    file_names = get_filenames(problem_name)
    filename = file_names['iris_data']
    return (dict(row) for row in DictReader(open(filename, 'r')))


def stream_data(problem_name):
    """
    :param problem_name: name of problem
    :return: stream to processed rows of house sales data
    """
    from cd4ml.problems import read_schema_file
    from pathlib import Path
    categorical_fields, numeric_fields = read_schema_file(Path(Path(__file__).parent, "raw_schema.json"))

    return (process_row(row, categorical_fields, numeric_fields, row_num)
            for row_num, row in enumerate(stream_raw(problem_name)))


def process_row(row, categorical_fields, numeric_fields, row_num):
    """
    Process a raw row of iris data and give it the right schema
    :param row: raw row
    :param schema: raw_schema_dict
    :param row_num: row_number
    :return: processed row
    """

    row_out = {k: row[k] for k in categorical_fields}

    for field in numeric_fields:
        row_out[field] = float_or_zero(row[field])

    row_out['row_num'] = row_num

    return row_out
