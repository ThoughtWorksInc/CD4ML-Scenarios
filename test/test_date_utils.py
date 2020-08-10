import cd4ml.utils.date_utils as du
import datetime


def test_parse_date_as_datetime_date():
    par = du.parse_date_as_datetime_date
    date_string = '6/18/12 12:04'
    result = par(date_string)
    expected = datetime.date(2012, 6, 18)
    assert result == expected

    par = du.parse_date_as_datetime_date
    assert par('8/25/04 23:00') == datetime.date(2004, 8, 25)
    assert par('08/25/04 23:00') == datetime.date(2004, 8, 25)
    assert par('08/25/04 00:00') == datetime.date(2004, 8, 25)
    assert par('08/25/84 00:00') == datetime.date(1984, 8, 25)
    assert par('08/5/84 00:00') == datetime.date(1984, 8, 5)
    assert par('08/05/84 00:00') == datetime.date(1984, 8, 5)

    date_string = '1975-05-01'
    result = par(date_string)
    expected = datetime.date(1975, 5, 1)
    assert result == expected

    date_string = '05-JAN-01'
    result = par(date_string)
    expected = datetime.date(2001, 1, 5)
    assert result == expected


def test_get_days_from_start_date():
    start_date = du.parse_date_as_datetime_date('1/1/18')
    current_date = du.parse_date_as_datetime_date('1/31/18')
    assert du.get_days_from_start_date(current_date, start_date) == 30


def test_convert_date_to_ymd():
    con = du.convert_date_to_ymd

    assert con('8/25/04') == '2004-08-25'
    assert con('8/25/04 23:00') == '2004-08-25'
    assert con('09-OCT-78') == '1978-10-09'


def test_add_to_date_string():
    ads = du.add_to_date_string
    assert ads('2018-03-20', years=0, months=0, days=0) == '2018-03-20'
    assert ads('2018-03-20') == '2018-03-20'
    assert ads('2018-03-20', years=1, months=-2, days=4) == '2019-01-24'
    assert ads('2018-03-20', days=365) == '2019-03-20'
    # Works with leap year
    assert ads('2018-03-20', days=365 * 4) == '2022-03-19'
    # just days more than 365, no leap years, 730 = 2 years
    assert ads('2017-03-20', years=0, months=0, days=730) == '2019-03-20'
    assert ads('2015-03-20', years=0, months=0, days=-730) == '2013-03-20'


def test_diff_days_date_strings():
    assert du.diff_days_date_strings('2008-03-31', '2008-03-31') == 0
    assert du.diff_days_date_strings('2008-03-31', '2009-03-31') == 365
    assert du.diff_days_date_strings('2009-03-31', '2008-03-31') == -365
    assert du.diff_days_date_strings('2000-01-01', '2004-01-01') == 4 * 365 + 1


def test_ymd_to_date_string():
    assert du.ymd_to_date_string((2020, 11, 5)) == '2020-11-05'
    assert du.ymd_to_date_string((2020, 1, 5)) == '2020-01-05'
    assert du.ymd_to_date_string((2020, 6, 23)) == '2020-06-23'


def test_date_to_ymd():
    date_string = '2020-02-12'
    year, month, day = du.date_to_ymd(date_string)
    assert year == 2020
    assert month == 2
    assert day == 12


def test_date_string_to_weekday():
    # Thursday March 26, 2020
    date_string = '2020-03-26'
    weekday = du.date_string_to_weekday(date_string)
    assert weekday == 3



