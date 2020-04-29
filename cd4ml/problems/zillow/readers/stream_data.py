from csv import DictReader
from cd4ml.filenames import file_names
from cd4ml.problems.zillow.config.ml_fields import get_ml_fields


def stream_raw(pipeline_params):
    """
    :param pipeline_params: pipeline_params data structure
    :return: stream to raw rows of Zillow data

    """
    assert pipeline_params['problem_name'] == 'zillow'

    year = pipeline_params['problem_params']['zillow_year']
    properties_filename = file_names['zillow_properties'].format(year=year)
    sales_filename = file_names['zillow_sales'].format(year=year)

    sales_lookup = {row['parcelid']: row for row in DictReader(open(sales_filename, 'r'))}

    properties = DictReader(open(properties_filename, 'r'))

    for row in properties:
        sales_data = sales_lookup[row['parcelid']]
        row['transaction_date'] = sales_data['transactiondate']
        row['logerror'] = sales_data['logerror']
        yield dict(row)


def stream_data(pipeline_params, with_descriptions=False):
    """
    :param pipeline_params: pipeline_params data structure
    :param with_descriptions: Default False, if True will show full
        descriptions. Just for interactive work.
    :return: stream to processed rows of Zillow data
    """
    if with_descriptions:
        mapper = get_description_mapper()
    else:
        def mapper(row_in):
            return process_row(row_in)

    return (mapper(row) for row in stream_raw(pipeline_params))


def get_data_dict():
    """
    Get the Zillow data dictionary field lookup
    :return: data dictionary from field to description
    """
    data_dict_file = file_names['zillow_data_dict_fields']
    data_dict = {row['Feature'].replace("'", ""): row['Description']
                 for row in DictReader(open(data_dict_file, 'r', encoding='utf-8-sig'))}

    data_dict['logerror'] = 'Logarithm of Zestimate/Price (target)'
    data_dict['transaction_date'] = 'Date of transactions'
    return data_dict


def get_description_mapper():
    """
    Interactive tool for viewing data with descriptions
    :return: function to map rows to ones with
        descriptions
    """
    data_dict = get_data_dict()

    def mapper(row):
        return {data_dict[k]: (k, v) for k, v in row.items()}

    return mapper


def float_or_zero(x):
    """
    :param x: any value
    :return: converted to float if possible, otherwise 0.0
    """
    try:
        return float(x)

    except ValueError:
        return 0.0


def process_row(row):
    """
    Process a raw row of Zillow data and give it the right schema
    :param row: raw row
    :return: processed row
    """
    ml_fields = get_ml_fields()
    catergorical_fields = list(ml_fields['categorical'].keys())
    numeric_fields = ml_fields['numerical']
    # Make sure there are no overlaps
    overlap = set(catergorical_fields).intersection(numeric_fields)
    assert len(overlap) == 0

    row_out = {k: row[k] for k in catergorical_fields}

    for field in numeric_fields:
        row_out[field] = float_or_zero(row[field])

    return row_out
