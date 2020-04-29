from cd4ml.utils import hash_to_uniform_random


def validate_splitting(pipeline_params):
    assert 'problem_params' in pipeline_params
    prob_params = pipeline_params['problem_params']
    assert 'identifier' in prob_params
    assert 'splitting' in prob_params
    assert 'random_seed' in prob_params

    splitting = prob_params['splitting']

    # check ordered properly
    assert splitting['training_random_start'] <= splitting['training_random_end']
    assert splitting['validation_random_start'] <= splitting['validation_random_end']

    # all within 0 to 1
    assert 0 <= splitting['training_random_start'] <= 1
    assert 0 <= splitting['training_random_end'] <= 1
    assert 0 <= splitting['validation_random_start'] <= 1
    assert 0 <= splitting['validation_random_end'] <= 1

    # no overlap in range
    one = splitting['training_random_start'] > splitting['validation_random_end']
    the_other = splitting['validation_random_start'] > splitting['training_random_end']
    assert one or the_other


def splitter(pipeline_params):
    validate_splitting(pipeline_params)
    identifier = pipeline_params['problem_params']['identifier']
    seed = pipeline_params['problem_params']['random_seed']
    splitting = pipeline_params['problem_params']['splitting']

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
