import pytest
from cd4ml.splitter import splitter, validate_splitting
from copy import deepcopy

problem_params_minimal = {
    'random_seed': 1299472653,
    'identifier': 'some_identifier',
    'splitting': {
        'training_random_start': 0.0,
        'training_random_end': 0.2,
        'validation_random_start': 0.6,
        'validation_random_end': 1.0
    }}

pipeline_params_minimal = {'problem_params': problem_params_minimal}


def test_validate_splitting_raises_assertions():
    validate_splitting(pipeline_params_minimal)

    with pytest.raises(AssertionError):
        validate_splitting({})

    with pytest.raises(AssertionError):
        validate_splitting({'problem_params': {}})

    with pytest.raises(AssertionError):
        validate_splitting({'problem_params': {'identifier': 0}})


def test_validate_splitting_check_ranges_0_1():
    params = deepcopy(pipeline_params_minimal)
    validate_splitting(params)
    with pytest.raises(AssertionError):
        params = deepcopy(pipeline_params_minimal)
        params['problem_params']['splitting']['training_random_start'] = -1.0
        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(pipeline_params_minimal)
        params['problem_params']['splitting']['training_random_start'] = 1.6
        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(pipeline_params_minimal)
        params['problem_params']['splitting']['training_random_start'] = 0.1
        params['problem_params']['splitting']['training_random_end'] = 0.06
        params['problem_params']['splitting']['validation_random_start'] = 0.5
        params['problem_params']['splitting']['validation_random_end'] = 0.6

        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(pipeline_params_minimal)
        params['problem_params']['splitting']['training_random_start'] = 0.0
        params['problem_params']['splitting']['training_random_end'] = 0.06
        params['problem_params']['splitting']['validation_random_start'] = 0.5
        params['problem_params']['splitting']['validation_random_end'] = 0.4

        validate_splitting(params)


def test_validate_splitting_check_ranges_overlap():
    params = deepcopy(pipeline_params_minimal)
    validate_splitting(params)
    with pytest.raises(AssertionError):
        params = deepcopy(pipeline_params_minimal)
        params['problem_params']['splitting']['training_random_start'] = 0.1
        params['problem_params']['splitting']['training_random_end'] = 0.3
        params['problem_params']['splitting']['validation_random_start'] = 0.2
        params['problem_params']['splitting']['validation_random_end'] = 0.7

        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(pipeline_params_minimal)
        params['problem_params']['splitting']['validation_random_start'] = 0.1
        params['problem_params']['splitting']['validation_random_end'] = 0.3
        params['problem_params']['splitting']['training_random_start'] = 0.2
        params['problem_params']['splitting']['training_random_end'] = 0.7
        validate_splitting(params)


def test_splitting_sanity_no_overlapping_sets():
    training_filter, validation_filter = splitter(pipeline_params_minimal)
    num = 1000
    data = [{'some_identifier': str(i)} for i in range(num)]
    data = data + data
    train = {i['some_identifier'] for i in data if training_filter(i)}
    valid = {i['some_identifier'] for i in data if validation_filter(i)}
    assert len(train.intersection(valid)) == 0

    # also check approximate size, these depends slightly on random seed above
    assert len(valid) > len(train)

    assert 180 <= len(train) <= 220
    assert 370 <= len(valid) <= 430
