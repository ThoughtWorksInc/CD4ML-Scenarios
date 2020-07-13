from cd4ml.app_utils import get_prediction


def test_get_prediction():
    item_numbers = ["99197", "105574", "1963838"]
    date_strings = ["2017-02-13", "2017-12-23"]
    for item_nbr in item_numbers:
        for date_string in date_strings:
            pred = get_prediction(item_nbr, date_string)
            print("item_nbr: %s, date: %s, pred: %s" % (item_nbr, date_string, pred))
