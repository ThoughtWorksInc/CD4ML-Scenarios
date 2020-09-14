import datetime
import arrow

from cd4ml.utils.memo import memo


@memo
def parse_date_to_arrow(date_string):
    first_part = date_string.split()[0]
    first_part = first_part.split(":")[0]

    try:
        format_string = 'M/D/YY'
        arrow_date = arrow.get(first_part, format_string)
    except arrow.parser.ParserError:
        try:
            format_string = 'DD-MMM-YY'
            arrow_date = arrow.get(first_part, format_string)
        except arrow.parser.ParserError:
            try:
                format_string = 'YYYY-MM-DD'
                arrow_date = arrow.get(first_part, format_string)
            except arrow.parser.ParserError:
                format_string = 'DDMMMYYYY'
                arrow_date = arrow.get(first_part, format_string)

    return arrow_date


@memo
def parse_date_as_datetime_date(date_string):
    return parse_date_to_arrow(date_string).date()


def get_days_from_start_date(current_date, start_date):
    diff_sec = (current_date - start_date).total_seconds()
    return diff_sec / (24 * 3600.0)


def get_day_range_dates(num_days, stride_days):
    first = datetime.date(2000, 1, 1)
    return [first + datetime.timedelta(days=x)
            for x in range(0, num_days * stride_days, stride_days)]


@memo
def convert_date_to_ymd(date):
    """
    :param date: a date string
    :return: date in 'YYYY-MM-DD' format (e.g. 1978-03-30)
    """
    date_format = 'YYYY-MM-DD'
    return parse_date_to_arrow(date).format(date_format)


def add_to_date_string(date_string, years=0, months=0, days=0):
    arrow_obj = parse_date_to_arrow(date_string)
    fmt = 'YYYY-MM-DD'
    return arrow_obj.shift(years=years, months=months, days=days).format(fmt)


def diff_days_date_strings(date_string_start, date_string_end):
    arrow_obj_start = parse_date_to_arrow(date_string_start)
    arrow_obj_end = parse_date_to_arrow(date_string_end)
    return (arrow_obj_end - arrow_obj_start).days


@memo
def date_string_to_date(date):
    year, month, day = date_to_ymd(date)
    return datetime.date(year, month, day)


@memo
def ymd_to_date_string(ymd):
    year, month, day = ymd
    return "%s-%s-%s" % (str(year), str(month).zfill(2), str(day).zfill(2))


@memo
def date_to_ymd(date_string):
    ymd = date_string.split('-')
    ymd = [int(i) for i in ymd]
    year, month, day = ymd
    return year, month, day


@memo
def ymd_to_weekday(ymd):
    date = datetime.datetime(ymd)
    return date.weekday()


@memo
def date_string_to_weekday(date_string):
    ymd = date_to_ymd(date_string)
    date = datetime.datetime(*ymd)
    return date.weekday()
