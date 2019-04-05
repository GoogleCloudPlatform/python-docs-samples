import pytest
from query_builder.domain_model.services.validation_service import (
    validate_runnable_query,
    assert_existing_query,
    validate_save_query
)
from query_builder.domain_model.dtos import (
    ReadTime,
    Step,
    Query,
    Threshold
)
from query_builder.domain_model.exceptions import (
    QBValidationError,
    QBNotFoundError
)


@pytest.mark.parametrize('duration', ['40w', '280d', '6720h', '403200m', '24192000s', '40w+2d'])
def test_validate_runnable_query_duration_valid(duration):
    # given
    step = Step(
        uuid='uuid',
        order=1,
        kind='ASSET',
        compare_duration=duration,
        threshold=Threshold(operator="le", value="10")
    )
    query = Query(
        uuid='uuid',
        steps=[step]
    )
    # when / then
    validate_runnable_query(query)


@pytest.mark.parametrize('duration', ['w', '1', '1hh', '1g', '1 w', '1w+', '1w-1d', '1w +1d'])
def test_validate_runnable_query_duration_invalid(duration):
    # given
    step = Step(
        uuid='uuid',
        order=1,
        kind='ASSET',
        compare_duration=duration,
        threshold=Threshold(operator="le", value="5")
    )
    query = Query(
        uuid='uuid',
        steps=[step]
    )
    expected_error_key = 'compareDuration1'
    expected_error_value = {
        'message' : 'Compare duration field invalid on step #1'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


@pytest.mark.parametrize('duration', ['40w', '280d', '6720h', '403200m', '24192000s', '40w+2d'])
def test_validate_runnable_query_ref_time_from_now_valid(duration):
    # given
    ref_time = ReadTime(
        _type='FROM_NOW',
        value=duration,
        zone=None
    )
    step = Step(
        uuid='uuid',
        order=1,
        kind='ASSET',
        read_time=ref_time,
        threshold=Threshold(operator="le", value="10")
    )
    query = Query(
        uuid='uuid',
        steps=[step]
    )
    # when / then
    validate_runnable_query(query)


@pytest.mark.parametrize('duration', ['w', '1', '1hh', '1g', '1 w', '1w+', '1w-1d', '1w +1d'])
def test_validate_runnable_query_ref_time_from_now_invalid(duration):
    # given
    ref_time = ReadTime(
        _type='FROM_NOW',
        value=duration,
        zone=None
    )
    step = Step(
        uuid='uuid',
        order=1,
        kind='ASSET',
        read_time=ref_time,
        threshold=Threshold(operator="le", value="10")
    )
    query = Query(
        uuid='uuid',
        steps=[step]
    )
    expected_error_key = 'readTimeValue1'
    expected_error_value = {
        'message' : 'Read time field invalid on step #1'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


@pytest.mark.parametrize('timestamp', ['2018-01-01T01:00:00+0200', '2018-01-01T01:00:00-0200'])
def test_validate_runnable_query_ref_time_timestamp_valid(timestamp):
    # given
    ref_time = ReadTime(
        _type='TIMESTAMP',
        value=timestamp,
        zone=None
    )
    step = Step(
        uuid='uuid',
        order=1,
        kind='ASSET',
        read_time=ref_time,
        threshold=Threshold(operator="ge", value="10")
    )
    query = Query(
        uuid='uuid',
        steps=[step]
    )
    # when / then
    validate_runnable_query(query)


@pytest.mark.parametrize('threshold_operator',['lt','le','eq','ne','ge','gt'])
def test_validate_runnable_query_with_threshold_operator(threshold_operator):
    # given
    step = Step(
        uuid='uuid',
        order=1,
        kind='ASSET',
        threshold=Threshold(operator=threshold_operator, value="10")
    )
    query = Query(
        uuid='uuid',
        steps=[step]
    )
    # when / then
    validate_runnable_query(query)


@pytest.mark.parametrize('timestamp', ['2018-02-31T01:00:00', '2018-02-31T01:00:00+0200', '2018/01/01T01:00:00-0200'])
def test_validate_runnable_query_ref_time_timestamp_invalid(timestamp):
    # given
    ref_time = ReadTime(
        _type='TIMESTAMP',
        value=timestamp,
        zone=None
    )
    step = Step(
        uuid='uuid',
        order=1,
        kind='ASSET',
        read_time=ref_time,
        threshold=Threshold(operator="ge", value="10")
    )
    query = Query(
        uuid='uuid',
        steps=[step]
    )
    expected_error_key = 'readTimeValue1'
    expected_error_value = {
        'message' : 'Read time field invalid on step #1'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


def test_assert_existing_query_not_ok():
    # given
    query = None
    uuid = ''
    expected_error = 'Query not found for uuid: '
    with pytest.raises(QBNotFoundError) as ex:
        # when
        assert_existing_query(uuid, query)
    # then
    assert ex.value.errors == expected_error


def test_assert_existing_query_ok():
    # given
    uuid = ''
    query = Query(
        uuid=uuid,
        description='Test query'
    )
    # when / then
    assert_existing_query(uuid, query)


def test_validate_runnable_query_no_steps():
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    query = Query(
        uuid=uuid
    )
    expected_error_key = 'steps'
    expected_error_value = {'message' : 'Required at least one step'}
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


def test_validate_runnable_query_no_threshold():
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET'
    )
    query = Query(
        uuid=uuid,
        steps=[step]
    )
    expected_error_key = 'threshold1'
    expected_error_value = {'message' : 'Threshold is empty on step #1'}
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


@pytest.mark.parametrize('operator', [None, 'GT', '_gt', 'ne '])
def test_validate_runnable_query_invalid_threshold_operator(operator):
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        threshold=Threshold(operator=operator, value='1')
    )
    query = Query(
        uuid=uuid,
        steps=[step]
    )
    expected_error_key = 'thresholdOperator1'
    expected_error_value = {
        'message' : "Threshold operator field invalid on step #1. Valid ['lt', 'le', 'eq', 'ne', 'ge', 'gt']"
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


def test_validate_runnable_query_empty_threshold_value():
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        threshold=Threshold(operator='gt', value=None)
    )
    query = Query(
        uuid=uuid,
        steps=[step]
    )
    expected_error_key = 'thresholdValue1'
    expected_error_value = {
        'message' : 'Threshold value field required on step #1'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


@pytest.mark.parametrize('value', [' 10', '\u00B2', '1_0', '1.0'])
def test_validate_runnable_query_invalid_threshold_value(value):
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        threshold=Threshold(operator='gt', value=value)
    )
    query = Query(
        uuid=uuid,
        steps=[step]
    )
    expected_error_key = 'thresholdValue1'
    expected_error_value = {
        'message' : 'Threshold value field invalid on step #1'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_runnable_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


def test_validate_save_query_empty_name():
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        threshold=Threshold(operator='gt', value='0')
    )
    query = Query(
        uuid=uuid,
        steps=[step],
        description='Description'
    )
    expected_error_key = 'name'
    expected_error_value = {
        'message' : 'Field name required'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_save_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


def test_validate_save_query_empty_description():
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        threshold=Threshold(operator='gt', value='0')
    )
    query = Query(
        uuid=uuid,
        steps=[step],
        name='Name'
    )
    expected_error_key = 'description'
    expected_error_value = {
        'message' : 'Field description required'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_save_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


def test_validate_save_query_not_runnable():
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET'
    )
    query = Query(
        uuid=uuid,
        steps=[step],
        name='Name',
        description='Description'
    )
    expected_error_key = 'threshold1'
    expected_error_value = {
        'message' : 'Threshold is empty on step #1'
    }
    with pytest.raises(QBValidationError) as ex:
        # when
        validate_save_query(query)
    # then
    assert len(ex.value.errors) == 1, 'Should return exactly 1 error'
    assert ex.value.errors[expected_error_key] == expected_error_value


def test_validate_save_query_ok():
    # given
    uuid = '57e43773-7890-4530-a667-443089a90adc'
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        threshold=Threshold(operator='gt', value='0')
    )
    query = Query(
        uuid=uuid,
        steps=[step],
        name='Name',
        description='Description'
    )
     # when / then
    validate_save_query(query)
