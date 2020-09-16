import pytest
from cd4ml.splitter import splitter, validate_splitting
from copy import deepcopy

ml_pipeline_params_minimal = {
    'identifier_field': 'some_identifier',
    'splitting': {
        'random_seed': 1299472653,
        'training_random_start': 0.0,
        'training_random_end': 0.2,
        'validation_random_start': 0.6,
        'validation_random_end': 1.0
    }}


def test_validate_splitting_raises_assertions():
    validate_splitting(ml_pipeline_params_minimal)

    with pytest.raises(AssertionError):
        validate_splitting({})

    with pytest.raises(AssertionError):
        validate_splitting({})

    with pytest.raises(AssertionError):
        validate_splitting({'identifier': 0})


def test_validate_splitting_check_ranges_0_1():
    params = deepcopy(ml_pipeline_params_minimal)
    validate_splitting(params)
    with pytest.raises(AssertionError):
        params = deepcopy(ml_pipeline_params_minimal)
        params['splitting']['training_random_start'] = -1.0
        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(ml_pipeline_params_minimal)
        params['splitting']['training_random_start'] = 1.6
        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(ml_pipeline_params_minimal)
        params['splitting']['training_random_start'] = 0.1
        params['splitting']['training_random_end'] = 0.06
        params['splitting']['validation_random_start'] = 0.5
        params['splitting']['validation_random_end'] = 0.6

        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(ml_pipeline_params_minimal)
        params['splitting']['training_random_start'] = 0.0
        params['splitting']['training_random_end'] = 0.06
        params['splitting']['validation_random_start'] = 0.5
        params['splitting']['validation_random_end'] = 0.4

        validate_splitting(params)


def test_validate_splitting_check_ranges_overlap():
    params = deepcopy(ml_pipeline_params_minimal)
    validate_splitting(params)
    with pytest.raises(AssertionError):
        params = deepcopy(ml_pipeline_params_minimal)
        params['splitting']['training_random_start'] = 0.1
        params['splitting']['training_random_end'] = 0.3
        params['splitting']['validation_random_start'] = 0.2
        params['splitting']['validation_random_end'] = 0.7

        validate_splitting(params)

    with pytest.raises(AssertionError):
        params = deepcopy(ml_pipeline_params_minimal)
        params['splitting']['validation_random_start'] = 0.1
        params['splitting']['validation_random_end'] = 0.3
        params['splitting']['training_random_start'] = 0.2
        params['splitting']['training_random_end'] = 0.7
        validate_splitting(params)


def test_splitting_sanity_no_overlapping_sets():
    training_filter, validation_filter = splitter(ml_pipeline_params_minimal)
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
