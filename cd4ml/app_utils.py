# TODO: remove some of this

products = {
    "99197": {
        "class": '1067',
        "family": 'GROCERY I',
        "perishable": '0'
    },
    "105574": {
        "class": '1045',
        "family": 'GROCERY I',
        "perishable": 0
    },
    "1963838": {
        "class": '3024',
        "family": 'CLEANING',
        "perishable": 0
    }
}

product_name_map = {
    "99197": "Milk",
    "105574": "Cheese",
    "1963838": "Soap"
}


def get_product_name_from_id(id):
    return product_name_map.get(id)
