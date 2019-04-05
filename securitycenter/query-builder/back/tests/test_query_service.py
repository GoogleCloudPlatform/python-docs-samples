import uuid
from datetime import datetime

from query_builder.domain_model.adapters import from_model_to_query_dto
from query_builder.domain_model.db import database
from query_builder.domain_model.dtos import Query as queryDto
from query_builder.domain_model.dtos import Step as stepDto
from query_builder.domain_model.dtos import Threshold, ReadTime
from query_builder.domain_model.models import Query, Step
from query_builder.domain_model.services.query_service import (
    save_query,
    list_queries,
    delete_query,
    get_query,
    update_query,
    update_query_notify,
    run_scheduled_queries,
    update_last_execution
)


def setup_function():
    queries = []
    mock_queries(queries)
    init_database()
    save_mocked_queries(queries)


def mock_queries(queries):
    steps = []
    ref_time = ReadTime(
        _type='FROM_NOW',
        value="1w",
        zone=None
    )
    steps.append(stepDto(uuid.uuid4(), order="1", kind="ASSET",
                         out_join="attribute.parent_id",
                         threshold=Threshold(operator="ge", value="15"),
                         read_time=ref_time, in_join=None,
                         filter_="attribute.asset_type = \"Firewall\" AND "
                                 "property.allowed : \"0-65535\"",
                         last_execution_result=5,
                         last_execution_status="fail"))

    steps.append(stepDto(uuid.uuid4(), order="2", kind="ASSET",
                         in_join="attribute.parent_id",
                         compare_duration="1w",
                         threshold=Threshold(operator="le", value="15"),
                         read_time=None, out_join=None,
                         filter_="attribute.asset_type = \"Instance\"",
                         last_execution_result=None,
                         last_execution_status="not executed"))

    queries.append(queryDto(uuid=uuid.uuid4(), name='number_1',
                            description='some description for first query',
                            owner='developer', topic='topic', steps=steps))

    queries.append(queryDto(uuid=uuid.uuid4(), name='number_2',
                            description='another description, but for second',
                            owner='manager', steps=steps))

    queries.append(queryDto(uuid=uuid.uuid4(), name='number_3',
                            description='this is the third query',
                            owner='intern', steps=steps))

    queries.append(queryDto(uuid=uuid.uuid4(), name='number_4',
                            description='4th is the last query that we have',
                            owner='admin', steps=steps))


def init_database():
    database.drop_tables([Step, Query], safe=True)
    database.create_tables([Step, Query], safe=True)


def save_mocked_queries(queries):
    for query in queries:
        save_query(query)
    database.close()


def test_list_queries_empty():
    Step.delete().execute()
    Query.delete().execute()
    queries = list_queries()

    assert queries[0] == []


def test_list_queries_paginated():
    result, total_size = list_queries(2, 2)

    assert len(result) == 2
    assert total_size == 4
    assert result[0].name == 'number_3'
    assert result[1].name == 'number_4'


def test_list_all_queries():
    result, total_size = list_queries()

    assert len(result) == 4
    assert total_size == 4
    assert result[0].name == 'number_1'
    assert result[1].name == 'number_2'


def test_list_query_text_one_found():
    result, total_size = list_queries(text='_1')

    assert len(result) == 1
    assert total_size == 1
    assert result[0].name == 'number_1'


def test_list_query_text_many_found():
    result, total_size = list_queries(text='number')

    assert len(result) == 4
    assert total_size == 4
    assert result[0].name == 'number_1'


def test_list_query_text_none_found():
    result, total_size = list_queries(text='test')

    assert len(result) == 0
    assert total_size == 0


def test_list_query_searching_description():
    result, total_size = list_queries(text='another')

    assert len(result) == 1
    assert total_size == 1
    assert result[0].description == 'another description, but for second'


def test_list_query_upper_case():
    result, total_size = list_queries(text='LAST QUERY')
    assert len(result) == 1
    assert total_size == 1
    assert result[0].description == '4th is the last query that we have'


def test_delete_query():
    result, total_size = list_queries(text="number_1")
    _id = result[0].uuid
    delete_query(_id)
    result, total_size = list_queries(text="number_1")
    assert total_size == 0


def test_get_query():
    result, _ = list_queries(text="number_2")
    query = get_query(result[0].uuid)
    assert query.name == "number_2"


def test_update_query():
    result, _ = list_queries(text="number_3")
    _id = result[0].uuid
    query = get_query(_id)
    description = "test update query"
    query.description = description
    # needed because update_query expect dto instead of model
    update_query(from_model_to_query_dto(query))
    query = get_query(_id)
    assert query.description == description


def test_update_query_notify():
    result, _ = list_queries(text="number_3")
    _id = result[0].uuid
    assert not result[0].send_notification
    update_query_notify(_id, True)
    query = get_query(_id)
    assert query.send_notification


def test_update_query_notify_without_flag():
    result, _ = list_queries(text="number_3")
    _id = result[0].uuid
    update_query_notify(_id, True)
    query = get_query(_id)
    assert query.send_notification
    update_query_notify(_id, None)
    query = get_query(_id)
    assert not query.send_notification


def test_step_saved():
    result, _ = list_queries(text="number_4")
    _id = result[0].uuid
    query = get_query(_id)
    assert len(query.steps) == 2


def test_run_scheduled_queries_each_minute(mocker):
    # given
    step = stepDto(uuid.uuid4(), order="1", kind="ASSET",
                   threshold=Threshold(operator="ge", value="15"),
                   read_time=None, in_join=None, out_join=None)
    queries = []
    queries.append(queryDto(uuid=uuid.uuid4(), name='even',
                            schedule='*/2 * * * *',
                            description='even minute', owner='manager',
                            steps=[step]))
    each_uuid = uuid.uuid4()
    queries.append(queryDto(uuid=each_uuid, name='each', schedule='* * * * *',
                            description='each minute', owner='manager',
                            steps=[step]))
    # Needed to force next run date on queries to near from mocked execution date
    with mocker.patch('query_builder.domain_model.services.query_service.__now',
                      return_value=datetime(
                          year=2018, month=6, day=20, hour=12, minute=0, second=59)):
        save_mocked_queries(queries)
    with mocker.patch('query_builder.domain_model.services.query_service.__now',
                      return_value=datetime(year=2018, month=6, day=20, hour=12, minute=1)):
        with mocker.mock_module.patch(
            'query_builder.domain_model.services.query_service.publish_queries_uuid') as mock:
            # when
            run_scheduled_queries()
            # then
            mock.assert_called_with([each_uuid])


def test_run_scheduled_queries_even_minute(mocker):
    # given
    step = stepDto(uuid.uuid4(), order="1", kind="ASSET",
                   threshold=Threshold(operator="ge", value="15"),
                   read_time=None, in_join=None, out_join=None)
    queries = []
    even_uuid = uuid.uuid4()
    queries.append(queryDto(uuid=even_uuid, name='even', schedule='*/2 * * * *',
                            description='even minute', owner='manager',
                            steps=[step]))
    queries.append(queryDto(uuid=uuid.uuid4(), name='each',
                            schedule='*/3 * * * *',
                            description='each minute', owner='manager',
                            steps=[step]))
    # Needed to force next run date on queries to near from mocked execution date
    with mocker.patch('query_builder.domain_model.services.query_service.__now',
                      return_value=datetime(
                          year=2018, month=6, day=20, hour=12, minute=0)):
        save_mocked_queries(queries)
    with mocker.patch('query_builder.domain_model.services.query_service.__now',
                      return_value=datetime(year=2018, month=6, day=20, hour=12, minute=2)):
        with mocker.mock_module.patch(
            'query_builder.domain_model.services.query_service.publish_queries_uuid') as mock:
            # when
            run_scheduled_queries()
            # then
            mock.assert_called_with([even_uuid])


def test_update_last_execution():
    result, _ = list_queries(text="number_4")
    _id = result[0].uuid
    query = from_model_to_query_dto(get_query(_id))
    steps_results = {}
    steps_results[1] = {"status":"SUCCESS", "responseSize" :8}
    steps_results[2] = {"status":"SUCCESS", "responseSize":4}
    execution_date = datetime.utcnow()
    update_last_execution(query, 10, steps_results, execution_date)

    query = get_query(_id)
    assert query.last_execution_result == 10
    assert query.steps[0].last_execution_status == "SUCCESS"
    assert query.steps[0].last_execution_result == 8
    assert query.steps[1].last_execution_status == "SUCCESS"
    assert query.steps[1].last_execution_result == 4
