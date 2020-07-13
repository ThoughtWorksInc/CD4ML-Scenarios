from cd4ml.date_utils import ymd_to_date_string, add_to_date_string, date_string_to_date
from cd4ml.read_data import stream_data


def get_max_date(pipeline_params):
    # batch step
    # '2017-08-15'
    print('Getting max date')
    max_date = max(date_string_to_date(row["date"]) for row in stream_data(pipeline_params))
    print('Max date: %s' % max_date)
    return max_date.strftime('%Y-%m-%d')


def get_cutoff_dates(pipeline_params):
    # batch step, 57 days usual
    days_back = pipeline_params['days_back']
    max_date = get_max_date(pipeline_params)
    date_cutoff = add_to_date_string(max_date, days=-days_back)
    return date_cutoff, max_date


def get_date_from_row(row):
    numbers = (int(row['year']), int(row['month']), int(row['day']))
    return ymd_to_date_string(numbers)


def train_filter(row, cutoff_date):
    return get_date_from_row(row) < cutoff_date


def validate_filter(row, cutoff_date, max_date):
    return cutoff_date <= get_date_from_row(row) <= max_date
