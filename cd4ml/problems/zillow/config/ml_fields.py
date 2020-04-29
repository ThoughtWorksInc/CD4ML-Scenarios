def get_ml_fields():
    categorical_n_levels_dict = {'airconditioningtypeid': 50,
                                 'architecturalstyletypeid': 50,
                                 'buildingqualitytypeid': 50,
                                 'buildingclasstypeid': 50,
                                 'decktypeid': 50,
                                 'threequarterbathnbr': 50,
                                 'fips': 50,
                                 'fireplaceflag': 50,
                                 'hashottuborspa': 50,
                                 'heatingorsystemtypeid': 50,
                                 'parcelid': 50,
                                 'pooltypeid10': 50,
                                 'pooltypeid2': 50,
                                 'pooltypeid7': 50,
                                 'propertycountylandusecode': 50,
                                 'propertylandusetypeid': 50,
                                 'propertyzoningdesc': 50,
                                 'rawcensustractandblock': 50,
                                 'censustractandblock': 50,
                                 'regionidcounty': 100,
                                 'regionidcity': 100,
                                 'regionidzip': 100,
                                 'regionidneighborhood': 50,
                                 'storytypeid': 50,
                                 'typeconstructiontypeid': 50,
                                 'taxdelinquencyflag': 50,
                                 'transaction_date': 50}

    numeric_fields = ['basementsqft', 'bathroomcnt', 'bedroomcnt', 'calculatedbathnbr',
                      'finishedfloor1squarefeet', 'calculatedfinishedsquarefeet',
                      'finishedsquarefeet6', 'finishedsquarefeet12', 'finishedsquarefeet13',
                      'finishedsquarefeet15', 'finishedsquarefeet50', 'fireplacecnt',
                      'fullbathcnt', 'garagecarcnt', 'garagetotalsqft', 'latitude', 'longitude',
                      'lotsizesquarefeet', 'numberofstories', 'poolcnt', 'poolsizesum',
                      'roomcnt', 'unitcnt', 'yardbuildingsqft17', 'yardbuildingsqft26',
                      'yearbuilt', 'taxvaluedollarcnt', 'structuretaxvaluedollarcnt',
                      'landtaxvaluedollarcnt', 'taxamount', 'assessmentyear', 'taxdelinquencyyear',
                      'logerror']

    target_field = 'logerror'

    ml_fields = {'categorical': categorical_n_levels_dict,
                 'numerical': numeric_fields,
                 'target_name': target_field}

    return ml_fields
