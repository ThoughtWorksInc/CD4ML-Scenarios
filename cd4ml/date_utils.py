import datetime
import arrow
import numpy as np
from cd4ml.memo import memo


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


# TODO: These needed for schema change
def get_rpr(r):
    x = r.get('date')
    if x is not None:
        return x
    else:
        return r['RPR_DT']


def get_smu(r):
    x = r.get('value')
    if x is not None:
        return x
    else:
        return r['USE_HR_MI']


def get_src(r):
    x = r.get('src_ind')
    if x is not None:
        return x
    else:
        return r['SRC_IND']


def get_days_utilz(record_list, ins_dt=None):
    parse = parse_date_as_datetime_date
    dates = [parse(get_rpr(r)) for r in record_list]
    utiliz = [get_smu(r) for r in record_list]
    src_inds = [get_src(r) for r in record_list]

    if ins_dt is None:
        # TODO: Old way where INS_DT was in each row
        start_date = list(set([parse(r['INS_DT']) for r in record_list]))
        assert len(start_date) == 1
        start_date = start_date[0]
    else:
        start_date = parse(ins_dt)

    days = [get_days_from_start_date(d, start_date) for d in dates]

    return np.array(days), np.array(utiliz), np.array(src_inds)


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
def ymd_to_date_string(ymd):
    year, month, day = ymd
    return "%s-%s-%s" % (str(year), str(month).zfill(2), str(day).zfill(2))
