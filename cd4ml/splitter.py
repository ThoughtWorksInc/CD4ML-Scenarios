from cd4ml.read_data import stream_raw_data
from cd4ml.date_utils import ymd_to_date_string, add_to_date_string


def get_date_from_row(row):
    numbers = (int(row['year']), int(row['month']), int(row['day']))
    return ymd_to_date_string(numbers)


def get_max_date():
    # batch step
    # '2017-08-15'
    print('Getting max date')
    max_date = '1500-01-01'
    stream = stream_raw_data()
    for row in stream:
        date = get_date_from_row(row)
        max_date = max(max_date, date)
    print('Max date: %s' % max_date)
    return max_date


def get_cutoff_dates(days_back):
    # batch step, 57 days usual
    max_date = get_max_date()
    date_cutoff = add_to_date_string(max_date, days=-days_back)
    return date_cutoff, max_date


def train_filter(row, cutoff_date):
    return get_date_from_row(row) < cutoff_date


def validate_filter(row, cutoff_date, max_date):
    return cutoff_date <= get_date_from_row(row) <= max_date
