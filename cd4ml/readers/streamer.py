from cd4ml.readers.file_reader import CSVDictionaryReader
from cd4ml.readers.postgres import PostgresReader
from cd4ml.filenames import file_names


class DataStreamer:
    def __init__(self, configuration_dictionary, use_filter=True):
        self.use_filter = use_filter
        self.items = {"99197", "105574", "1963838"}

        if "file" in configuration_dictionary["type"]:
            self.strategy = CSVDictionaryReader(file_names['raw_data'])

        elif "postgres" in configuration_dictionary["type"]:
            host = configuration_dictionary["host"]
            username = configuration_dictionary["username"]
            password = configuration_dictionary["password"]
            database = configuration_dictionary["database"]
            self.strategy = PostgresReader(host, username, password, database)
        else:
            raise ValueError("Configuration dictionary does not contain a valid 'type', must be one of ['file', "
                             "'postgres']")

    def stream_data(self):
        if self.use_filter:
            filter_func = self._in_small_item_list
        else:
            def filter_func(_):
                return True

        data = self.strategy.read_data()
        return (dict(row) for row in data if filter_func(row))

    def close(self):
        self.strategy.close()

    def _in_small_item_list(self, row):
        return row['item_nbr'] in self.items

    @staticmethod
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
