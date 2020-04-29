from cd4ml.problems.shopping.readers.file_reader import CSVDictionaryReader
from cd4ml.problems.shopping.readers.postgres import PostgresReader


class DataStreamer:
    def __init__(self, data_source):
        if data_source == "file":
            self.reader = CSVDictionaryReader()

        elif data_source == "postgres":
            self.reader = PostgresReader()
        else:
            raise ValueError("data_source must be 'file' or 'postgres'")

    def stream_data(self):
        return (dict(row) for row in self.reader.stream_data())


def process(row_in):
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
            'dayoff': int(row_in['dayoff'] == 'True')}


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


def stream_data(pipeline_params, apply_filter=True):
    """
    The only way that data should be read in the pipeline is by calling this
    and reading from the stream
    :param pipeline_params: parameters for everything in pipeline
    :param apply_filter: if true (default), filter the rows
    :return: a stream of data from a source specified in pipeline_params
    """
    data_source = pipeline_params['problem_params']['data_source']
    data_streamer = DataStreamer(data_source)
    data = data_streamer.stream_data()
    for row in data:
        if apply_filter and not filter_func(row):
            # does not pass filter, skip
            continue

        yield process(row)
