from datetime import datetime

import query_builder.domain_model.adapters as adapters

from query_builder.domain_model.dtos import SimpleQuery

from .helpers.query_objects import (
    QUERY_DTO,
    QUERY_DTO_WITH_LAST_EXECUTION,
    QUERY_MODEL,
    STEPS_DTO_1,
    STEPS_MODEL_1,
    QUERY_JSON_STEP,
    QUERY_JSON_WITH_STEPS,
    QUERY_JSON_WITH_STEPS_WITH_LAST_EXECUTION,
    QUERY_JSON_WITH_STEPS_WITHOUT_LAST_EXECUTION
)


def test_from_model_to_query_dto():
    dto_result = adapters.from_model_to_query_dto(QUERY_MODEL)
    assert dto_result.uuid == QUERY_DTO.uuid
    assert dto_result.name == QUERY_DTO.name
    assert dto_result.owner == QUERY_DTO.owner
    assert dto_result.timestamp == QUERY_DTO.timestamp
    assert dto_result.topic == QUERY_DTO.topic
    assert dto_result.description == QUERY_DTO.description


def test_from_model_to_step_dto():
    dto_result = adapters.from_model_to_step_dto(QUERY_MODEL.uuid, STEPS_MODEL_1)
    assert dto_result.uuid == STEPS_DTO_1.uuid
    assert dto_result.filter == STEPS_DTO_1.filter
    assert dto_result.out_join == STEPS_DTO_1.out_join
    assert dto_result.order == STEPS_DTO_1.order
    assert dto_result.kind == STEPS_DTO_1.kind
    assert dto_result.in_join == STEPS_DTO_1.in_join
    assert dto_result.compare_duration == STEPS_DTO_1.compare_duration
    assert dto_result.read_time.value == STEPS_DTO_1.read_time.value
    assert dto_result.threshold.value == STEPS_DTO_1.threshold.value
    assert dto_result.last_execution_result == STEPS_DTO_1.last_execution_result
    assert dto_result.last_execution_status == STEPS_DTO_1.last_execution_status


def test_from_json_to_step_dto():
    dto_result = adapters.from_json_to_step_dto(
        QUERY_DTO.uuid, QUERY_JSON_STEP)
    assert dto_result.uuid == STEPS_DTO_1.uuid
    assert dto_result.filter == STEPS_DTO_1.filter
    assert dto_result.out_join == STEPS_DTO_1.out_join
    assert dto_result.order == STEPS_DTO_1.order
    assert dto_result.kind == STEPS_DTO_1.kind
    assert dto_result.in_join == STEPS_DTO_1.in_join
    assert dto_result.compare_duration == STEPS_DTO_1.compare_duration
    assert dto_result.read_time.value == STEPS_DTO_1.read_time.value
    assert dto_result.threshold.value == STEPS_DTO_1.threshold.value


def test_from_json_to_query_dto():
    dto_result = adapters.from_json_to_query_dto(
        QUERY_JSON_WITH_STEPS_WITH_LAST_EXECUTION)
    assert dto_result.uuid == QUERY_DTO_WITH_LAST_EXECUTION.uuid
    assert dto_result.name == QUERY_DTO_WITH_LAST_EXECUTION.name
    assert dto_result.owner == QUERY_DTO_WITH_LAST_EXECUTION.owner
    assert dto_result.timestamp == QUERY_DTO_WITH_LAST_EXECUTION.timestamp
    assert dto_result.topic == QUERY_DTO_WITH_LAST_EXECUTION.topic
    assert dto_result.description == QUERY_DTO_WITH_LAST_EXECUTION.description
    assert dto_result.send_notification == QUERY_DTO_WITH_LAST_EXECUTION\
        .send_notification
    assert dto_result.last_execution_date == QUERY_DTO_WITH_LAST_EXECUTION\
        .last_execution_date
    assert dto_result.last_execution_result == QUERY_DTO_WITH_LAST_EXECUTION\
        .last_execution_result
    assert dto_result.last_execution_status == QUERY_DTO_WITH_LAST_EXECUTION\
        .last_execution_status


def test_from_json_to_query_dto_with_empty_values_into_last_execution():
    dto_result = adapters.from_json_to_query_dto(QUERY_JSON_WITH_STEPS)
    assert dto_result.uuid == QUERY_DTO.uuid
    assert dto_result.name == QUERY_DTO.name
    assert dto_result.owner == QUERY_DTO.owner
    assert dto_result.timestamp == QUERY_DTO.timestamp
    assert dto_result.topic == QUERY_DTO.topic
    assert dto_result.description == QUERY_DTO.description
    assert dto_result.send_notification == QUERY_DTO.send_notification
    assert dto_result.last_execution_status is None
    assert dto_result.last_execution_result is None
    assert dto_result.last_execution_date is None


def test_from_json_to_query_dto_without_last_execution():
    dto_result = adapters.from_json_to_query_dto(
        QUERY_JSON_WITH_STEPS_WITHOUT_LAST_EXECUTION)
    assert dto_result.uuid == QUERY_DTO.uuid
    assert dto_result.name == QUERY_DTO.name
    assert dto_result.owner == QUERY_DTO.owner
    assert dto_result.timestamp == QUERY_DTO.timestamp
    assert dto_result.topic == QUERY_DTO.topic
    assert dto_result.description == QUERY_DTO.description
    assert dto_result.send_notification == QUERY_DTO.send_notification
    assert dto_result.last_execution_status is None
    assert dto_result.last_execution_result is None
    assert dto_result.last_execution_date is None


def test_from_model_to_query_json():
    json_result = adapters.from_model_to_query_json(QUERY_MODEL)
    assert json_result['uuid'] == QUERY_JSON_WITH_STEPS['uuid']
    assert json_result['name'] == QUERY_JSON_WITH_STEPS['name']
    assert json_result['owner'] == QUERY_JSON_WITH_STEPS['owner']
    assert json_result['topic'] == QUERY_JSON_WITH_STEPS['topic']
    assert json_result['description'] == QUERY_JSON_WITH_STEPS['description']
    assert json_result['steps'][0]["kind"] == QUERY_JSON_WITH_STEPS['steps'][0]['kind']
    assert json_result['steps'][0]['threshold']['operator'] == QUERY_JSON_WITH_STEPS['steps'][0]['threshold']['operator']
    assert json_result['steps'][0]['lastExecution']['result'] == QUERY_JSON_WITH_STEPS['steps'][0]['lastExecution']['result']
    assert json_result['steps'][0]['lastExecution']['status'] == QUERY_JSON_WITH_STEPS['steps'][0]['lastExecution']['status']


def test_from_model_to_step_json():
    json_result = adapters.from_model_to_step_json(QUERY_MODEL)
    assert json_result[0]['kind'] == QUERY_JSON_STEP['kind']
    assert json_result[0]['order'] == QUERY_JSON_STEP['order']
    assert json_result[0]['outJoin'] == QUERY_JSON_STEP['outJoin']
    assert json_result[0]['readTime']['value'] == QUERY_JSON_STEP['readTime']['value']
    assert json_result[0]['threshold']['value'] == QUERY_JSON_STEP['threshold']['value']
    assert json_result[0]['threshold']['operator'] == QUERY_JSON_STEP['threshold']['operator']
    assert json_result[0]['lastExecution']['result'] == QUERY_JSON_STEP['lastExecution']['result']
    assert json_result[0]['lastExecution']['status'] == QUERY_JSON_STEP['lastExecution']['status']


def test_from_model_to_simple_queries_json():
    # given
    queries = [
        SimpleQuery(
            uuid='74b8f5a8-9829-48fb-9acc-6377ecf5149a',
            name='query_test1',
            description='testing1',
            owner='example@example.org',
            timestamp=datetime(
                year=2018,
                month=6,
                day=28,
                hour=15,
                minute=0,
                second=38),
            mark={
                'scc_query_74b8f5a8-9829-48fb-9acc-6377ecf5149a':
                'working_74b8f5a8-9829-48fb-9acc-6377ecf5149a'
            },
            next_run=datetime(
                year=2018,
                month=6,
                day=28,
                hour=15,
                minute=2),
            last_execution_date=None,
            last_execution_result=None,
            last_execution_status=None,
            send_notification=True
        ),
        SimpleQuery(
            uuid='74b8f5a8-9829-48fb-9acc-6377ecf5149c',
            name='query_test2',
            description='testing2',
            owner='example@example.org',
            timestamp=datetime(
                year=2018,
                month=6,
                day=28,
                hour=15,
                minute=0,
                second=57),
            mark={
                'scc_query_74b8f5a8-9829-48fb-9acc-6377ecf5149c':
                'working_74b8f5a8-9829-48fb-9acc-6377ecf5149c'
            },
            last_execution_date=datetime(2018, 7, 10, 15, 33, 58),
            last_execution_result=5,
            last_execution_status="fail"
        )
    ]
    expected = {
        "queries": [
            {
                "description": "testing1",
                "mark": {
                    "scc_query_74b8f5a8-9829-48fb-9acc-6377ecf5149a":
                    "working_74b8f5a8-9829-48fb-9acc-6377ecf5149a"
                },
                "name": "query_test1",
                "nextRun": "2018-06-28T15:02:00",
                "owner": "example@example.org",
                "timestamp": "2018-06-28T15:00:38",
                "uuid": "74b8f5a8-9829-48fb-9acc-6377ecf5149a",
                "lastExecution": {"date": None, "result": None, "status": None},
                "sendNotification": True
            },
            {
                "description": "testing2",
                "mark": {
                    "scc_query_74b8f5a8-9829-48fb-9acc-6377ecf5149c":
                    "working_74b8f5a8-9829-48fb-9acc-6377ecf5149c"
                },
                "name": "query_test2",
                "nextRun": None,
                "owner": "example@example.org",
                "timestamp": "2018-06-28T15:00:57",
                "uuid": "74b8f5a8-9829-48fb-9acc-6377ecf5149c",
                "lastExecution": {"date":"2018-07-10T15:33:58", "result":5, "status":"fail"},
                "sendNotification": False
            }
        ],
        "total": 2
    }
    # when
    result = adapters.from_model_to_simple_queries_json(queries, len(queries))
    # then
    assert expected == result
