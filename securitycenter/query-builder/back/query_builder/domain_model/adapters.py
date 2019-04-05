from datetime import datetime as dt
from query_builder.domain_model.dtos import (
    Query as DtoQuery,
    Step as DtoStep,
    ReadTime as DtoReadTime,
    Threshold as DtoThreshold
)
from query_builder.domain_model.models import Step


def from_model_to_step_dto(uuid, step):
    in_join = None
    if step.in_value:
        in_join = step.in_value

    out_join = None
    if step.out_value:
        out_join = step.out_value

    read_time = None
    if step.read_time_value:
        read_time = DtoReadTime(
            step.read_time_type,
            step.read_time_value,
            step.read_time_zone
        )
    compare_duration = None
    if step.compare_duration:
        compare_duration = step.compare_duration

    filter_ = None
    if step.filter:
        filter_ = step.filter

    threshold = None
    if step.threshold_value:
        threshold = DtoThreshold(
            step.threshold_operator, step.threshold_value)

    dto = DtoStep(
        uuid,
        order=step.order,
        kind=step.scc_resource_type,
        in_join=in_join,
        out_join=out_join,
        read_time=read_time,
        compare_duration=compare_duration,
        threshold=threshold,
        last_execution_status=step.last_execution_status,
        last_execution_result=step.last_execution_result,
        filter_=filter_
    )
    return dto


def from_model_to_query_dto(query_model):
    steps = []
    for step in query_model.steps:
        steps.append(from_model_to_step_dto(query_model.uuid, step))

    dto = DtoQuery(
        uuid=query_model.uuid,
        name=query_model.name,
        description=query_model.description,
        owner=query_model.owner,
        topic=query_model.topic,
        timestamp=query_model.timestamp,
        steps=steps,
        schedule=query_model.schedule,
        send_notification=query_model.send_notification)
    return dto


def from_json_to_step_dto(uuid, json_step):

    in_join = None
    if 'inJoin' in json_step:
        in_join = json_step['inJoin']

    out_join = None
    if 'outJoin' in json_step:
        out_join = json_step['outJoin']

    read_time = None
    if 'readTime' in json_step:
        read_time = DtoReadTime(
            json_step['readTime']['type'],
            json_step['readTime']['value'],
            json_step['readTime']['timeZone'] if 'timeZone' in json_step['readTime'] else ''
        )

    threshold = None
    if 'threshold' in json_step:
        threshold = DtoThreshold(
            json_step['threshold']['operator'], json_step['threshold']['value'])

    dto = DtoStep(
        uuid,
        order=json_step.get('order', None),
        kind=json_step.get('kind', None),
        in_join=in_join,
        out_join=out_join,
        read_time=read_time,
        compare_duration=json_step.get('compareDuration', None),
        threshold=threshold,
        filter_=json_step.get('filter', None)
    )
    return dto


def from_json_to_query_dto(json_query):
    list_steps = []
    for step in json_query['steps']:
        list_steps.append(from_json_to_step_dto(json_query['uuid'], step))

    topic = None
    if 'topic' in json_query:
        topic = json_query['topic']

    query_dto = DtoQuery(
        json_query.get('uuid', None),
        name=json_query['name'],
        description=json_query['description'],
        owner=json_query['owner'] if 'owner' in json_query else '',
        send_notification=json_query['sendNotification'] if 'sendNotification' in json_query else False,
        steps=list_steps,
        topic=topic,
        schedule=json_query.get('schedule', None),
        last_execution_date=__parse_datetime(json_query.get('lastExecution')
                                             .get('date'))
        if json_query.get('lastExecution') and
        json_query.get('lastExecution').get('date') else None,
        last_execution_result=json_query.get('lastExecution').get('result')
        if json_query.get('lastExecution') else None,
        last_execution_status=json_query.get('lastExecution').get('status')
        if json_query.get('lastExecution') else None
    )

    return query_dto


def from_model_to_query_json(query):
    obj = {}
    if query:
        steps = from_model_to_step_json(query)
        obj = {
            "name": query.name,
            "description": query.description,
            "owner": query.owner,
            "uuid": query.uuid,
            "steps": steps,
            "schedule": query.schedule,
            "sendNotification": query.send_notification,
            "lastExecution": {
                "date": query.last_execution_date.isoformat() if query.last_execution_date else None,
                "result": query.last_execution_result,
                "status": query.last_execution_status
            }

        }
        if query.topic:
            obj['topic'] = query.topic
    return obj


def from_model_to_step_json(query):
    steps = []
    for step in query.steps:
        step_data = {
            "order": step.order,
            "kind": step.scc_resource_type
        }
        if step.filter:
            step_data['filter'] = step.filter
        if step.read_time_value:
            step_data['readTime'] = {
                "type": step.read_time_type,
                "value": step.read_time_value,
                "timeZone": step.read_time_zone
            }
        else:
            step_data['readTime'] = {}

        if step.compare_duration:
            step_data['compareDuration'] = step.compare_duration

        if step.in_value:
            step_data['inJoin'] = step.in_value

        if step.out_value:
            step_data['outJoin'] = step.out_value

        if step.threshold_operator:
            step_data['threshold'] = {
                "operator": step.threshold_operator,
                "value": step.threshold_value
            }

        if step.last_execution_status:
            step_data['lastExecution'] = {
                "result": step.last_execution_result,
                "status": step.last_execution_status
            }

        steps.append(step_data)
    return steps


def from_model_to_simple_queries_json(queries, total):
    simple_queries = []
    for query in queries:
        obj = {
            'uuid': query.uuid,
            'name': query.name,
            'description': query.description,
            'timestamp': query.timestamp.isoformat(),
            'owner': query.owner,
            'mark': query.mark,
            'nextRun': query.next_run.isoformat() if query.next_run else None,
            'lastExecution':{
                "date": query.last_execution_date.isoformat() if query.last_execution_date else None,
                "status": query.last_execution_status,
                "result": query.last_execution_result
            },
            'sendNotification': query.send_notification
        }
        simple_queries.append(obj)
    results = {
        'total': total,
        'queries': simple_queries
    }

    return results


def from_dto_to_step_model(step_dto, model_query):
    return Step(
        order=step_dto.order,
        scc_resource_type=step_dto.kind,
        filter=step_dto.filter,
        read_time_type=step_dto.read_time.get_type(
        ) if step_dto.read_time else None,
        read_time_value=step_dto.read_time.value if step_dto.read_time else None,
        read_time_zone=step_dto.read_time.zone if step_dto.read_time else None,
        compare_duration=step_dto.compare_duration,
        in_value=step_dto.in_join,
        out_value=step_dto.out_join,
        threshold_operator=step_dto.threshold.operator if step_dto.threshold else None,
        threshold_value=step_dto.threshold.value if step_dto.threshold else None,
        last_execution_result=step_dto.last_execution_result if step_dto.last_execution_result else None,
        last_execution_status=step_dto.last_execution_status if step_dto.last_execution_status else None,
        query=model_query
    )


def __parse_datetime(datetime):
    return dt.strptime(datetime, '%Y-%m-%dT%H:%M:%S')
