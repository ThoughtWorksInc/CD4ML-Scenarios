from cd4ml.utils.utils import float_or_zero


def base_record_to_feature(base_feature, lookup, feature):
    results = lookup.get(base_feature)
    if results is None:
        return None
    else:
        return results[feature]


def date_to_ymd(date):
    date_string = str(date)
    year, month, day = date_string[0:4], date_string[4:6], date_string[6:8]
    return int(year), int(month), int(day)


def date_to_day_of_week(record, lookup):
    return base_record_to_feature(record['date'], lookup, 'dayofweek')


def date_to_day_off(record, lookup):
    return float_or_zero(base_record_to_feature(record['date'], lookup, 'dayoff') == 'True')


def date_to_days_until_end(record, lookup):
    return float_or_zero(base_record_to_feature(record['date'], lookup, 'days_til_end_of_data'))


def item_nbr_to_product_class(record, lookup):
    return base_record_to_feature(record['item_nbr'], lookup, 'class')


def item_nbr_to_product_family(record, lookup):
    return base_record_to_feature(record['item_nbr'], lookup, 'family')


def item_nbr_to_perishable(record, lookup):
    return int(base_record_to_feature(record['item_nbr'], lookup, 'perishable'))

# derive
# from date: year, month, day, dayofweek, days_til_end_of_data, dayoff
# from item_nbr: family, class, perishable from item_nbr
