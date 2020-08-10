from cd4ml.utils.utils import hash_to_uniform_random


def validate_splitting(ml_pipeline_params):
    """
    Validate the splitting data structure
    It's important to get this right to ensure you are never
    validating data that you trained with (a common error in ML).
    Either raises an assertion or passes
    :param ml_pipeline_params: pipeline_params data structure
    :return: None
    """

    assert 'splitting' in ml_pipeline_params
    splitting = ml_pipeline_params['splitting']

    # check ordered properly
    assert splitting['training_random_start'] <= splitting['training_random_end']
    assert splitting['validation_random_start'] <= splitting['validation_random_end']

    # all within 0 to 1
    assert 0 <= splitting['training_random_start'] <= 1
    assert 0 <= splitting['training_random_end'] <= 1
    assert 0 <= splitting['validation_random_start'] <= 1
    assert 0 <= splitting['validation_random_end'] <= 1

    # no overlap in range
    one = splitting['training_random_start'] >= splitting['validation_random_end']
    the_other = splitting['validation_random_start'] >= splitting['training_random_end']
    assert one or the_other


def splitter(ml_pipeline_params):
    identifier = ml_pipeline_params['identifier_field']
    splitting = ml_pipeline_params.get('splitting')

    if splitting is None:
        return None, None
    else:
        validate_splitting(ml_pipeline_params)

    seed = splitting['random_seed']

    train_start = splitting['training_random_start']
    train_end = splitting['training_random_end']
    validation_start = splitting['validation_random_start']
    validation_end = splitting['validation_random_end']

    def training_filter(row):
        hash_val = hash_to_uniform_random(row[identifier], seed)
        assert 0 <= hash_val < 1
        return train_start <= hash_val < train_end

    def validation_filter(row):
        hash_val = hash_to_uniform_random(row[identifier], seed)
        assert 0 <= hash_val < 1
        return validation_start <= hash_val < validation_end

    return training_filter, validation_filter
