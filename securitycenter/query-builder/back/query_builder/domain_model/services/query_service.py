import os
from datetime import datetime
from croniter import croniter

import query_builder.application.default_settings as default_settings
from query_builder.domain_model.dtos import SimpleQuery
from query_builder.domain_model.adapters import (
    from_model_to_query_dto,
    from_dto_to_step_model
)
from query_builder.domain_model.services.pubsub_service import publish_uuid_to_clean
from .configuration_service import is_production_environment, get_organization_id
from .scc_service import (
    process_scc_query,
    build_mark_from_id,
    mark_to_query_filed,
    build_temp_mark_from_id
)
from .pubsub_service import publish_queries_uuid
from .validation_service import (
    validate_runnable_query,
    assert_existing_query,
    validate_save_query
)

from ..models import Query, Step
from ..db import database

LOGGER = default_settings.configure_logger('query_service')

SCC_URL_LINK_TEMPLATE = "https://console.cloud.google.com/security/{}s?organizationId={}"
SCC_URL_LINK_GENERIC_TEMPLATE = "https://console.cloud.google.com/security/?organizationId={}"


def run_query_by_uuid(uuid):
    query_model = get_query(uuid)
    assert_existing_query(uuid, query_model)
    dto = from_model_to_query_dto(query_model)
    LOGGER.info("run_query_by_uuid - uuid: %s", uuid)
    return run_query(dto)


def update_last_execution(query, last_execution_query_result, steps_result, execution_date):
    LOGGER.info("update_last_execution - uuid: %s, last_execution_query_result: %s",
                query.uuid, last_execution_query_result
               )
    with database.atomic():
        query_ = (
            Query.update(
                {
                    Query.last_execution_result: last_execution_query_result,
                    Query.last_execution_date: execution_date,
                    Query.last_execution_status: steps_result[len(steps_result)]["status"]
                }
            )
            .where(Query.uuid == query.uuid)
        )
        query_.execute()
        update_last_execution_steps(query, steps_result)

def update_last_execution_steps(query, steps_result):
    for step in query.steps:
        step_ = (
            Step.update({
                Step.last_execution_result: steps_result[step.order]["responseSize"],
                Step.last_execution_status: steps_result[step.order]["status"]
            }).where(Step.query == step.uuid and Step.order == step.order)
            )
        step_.execute()

def update_query_notify(uuid, flag):
    query = get_query(uuid)
    assert_existing_query(uuid, query)

    query = (Query
             .update({
                 Query.send_notification: bool(flag),
                 Query.timestamp: __now()
             })
             .where(Query.uuid == query.uuid))
    query.execute()

    LOGGER.info('Query with id %s updated notification flag to %s', uuid, flag)


def run_query(query_dto, mode="execution"):
    LOGGER.info("run_query - working_marks: %s", query_dto)
    validate_runnable_query(query_dto)

    if mode == "draft" or not is_production_environment():
        working_marks = build_temp_mark_from_id(query_dto.uuid)
    else:
        working_marks = build_mark_from_id(query_dto.uuid)

    LOGGER.info(working_marks)
    result_size, result_kind, step_results, execution_date = process_scc_query(
        query_dto,
        working_marks,
        mode
    )
    if mode == "execution":
        update_last_execution(query_dto, result_size, step_results, execution_date)

    LOGGER.info("run_query - working_marks: %s", working_marks)
    return (
        query_dto.uuid,
        result_size,
        build_url(result_kind),
        mark_to_query_filed(working_marks),
        step_results
    )


def clean_up_marks(uuid_to_clean):
    publish_uuid_to_clean(uuid_to_clean)


def save_query(query):
    LOGGER.info("save_query - uuid: %s", query.uuid)
    validate_save_query(query)
    with database.atomic():
        saved_query = Query.create(
            uuid=query.uuid,
            name=query.name,
            description=query.description,
            owner=query.owner,
            topic=query.topic,
            timestamp=__now(),
            schedule=query.schedule,
            next_run=__get_next_query_run(
                schedule=query.schedule, base_datetime=__now()) if query.schedule else None,
            send_notification=query.send_notification,
            last_execution_date=query.last_execution_date,
            last_execution_result=query.last_execution_result,
            last_execution_status=query.last_execution_status,
        )
        saved_query.save()
        steps = []
        for step_dto in query.steps:
            steps.append(from_dto_to_step_model(step_dto, saved_query))
        for step in steps:
            step.save()

    return saved_query


def get_query(uuid):
    LOGGER.info("get_query - uuid: %s", uuid)
    return Query.get_or_none(Query.uuid == uuid)


def delete_query(uuid):
    LOGGER.info("delete_query - uuid: %s", uuid)
    with database.atomic():
        Step.delete().where(Step.query_id == uuid).execute()
        Query.delete().where(Query.uuid == uuid).execute()


def update_query(_query):
    LOGGER.info("update_query - uuid: %s", _query.uuid)
    with database.atomic():
        delete_query(_query.uuid)
        save_query(_query)


def list_queries(page=None, page_size=None, text=''):
    LOGGER.info("list_queries - page: %s, page_size: %s, text: %s",
                page, page_size, text)
    queries = get_queries(page, page_size, text)
    simple_queries = []
    total = get_total_queries(text)
    for query in queries:
        mark = build_mark_from_id(query.uuid)
        simple_queries.append(
            SimpleQuery(
                uuid=query.uuid,
                name=query.name,
                timestamp=query.timestamp,
                description=query.description,
                owner=query.owner,
                mark=mark_to_query_filed(mark),
                next_run=query.next_run,
                last_execution_date=query.last_execution_date,
                last_execution_result=query.last_execution_result,
                last_execution_status=query.last_execution_status,
                send_notification=query.send_notification))
    return simple_queries, total


def get_queries(page, page_size, text):
    LOGGER.info("get_queries - page: %s, page_size: %s, text: %s",
                page, page_size, text)
    if(page is not None and page_size is not None):
        return Query.select().paginate(page, page_size).where(
            Query.name.contains(text) | Query.description.contains(text) | Query.owner.contains(text)
        ).order_by(Query.name)
    return __get_queries(text)


def get_total_queries(text):
    LOGGER.info("get_total_queries - text: %s", text)
    return __get_queries(text).count()


def run_scheduled_queries():
    """Get the scheduled queries to run and publish their uuid on topic to be executed"""
    with database.atomic():
        queries_to_run = __get_scheduled_queries()
        if queries_to_run:
            publish_queries_uuid(queries_to_run)


def __get_scheduled_queries():
    exec_datetime = __now()
    LOGGER.info('run_scheduled_queries called at: %s', exec_datetime)

    # Get queries scheduled to run now
    queries_to_run = []
    for uuid_schedule in Query.select(
            Query.uuid, Query.schedule).where(Query.next_run <= exec_datetime):
        queries_to_run.append(uuid_schedule.uuid)
        LOGGER.info('Query to run: %s, schedule: %s',
                    uuid_schedule.uuid,
                    uuid_schedule.schedule)
        # Update the next_run based on schedule cron expression
        query = (Query
                 .update({
                     Query.next_run: __get_next_query_run(uuid_schedule.schedule,
                                                          exec_datetime)
                 })
                 .where(Query.uuid == uuid_schedule.uuid))
        query.execute()

    return queries_to_run


def __get_queries(text):
    return Query.select().where(
        Query.name.contains(text) | Query.description.contains(text) | Query.owner.contains(text)
    ).order_by(Query.name)


def build_url(kind):
    if kind:
        return SCC_URL_LINK_TEMPLATE.format(
            kind.lower(),
            get_organization_id())
    return SCC_URL_LINK_GENERIC_TEMPLATE.format(get_organization_id())


def __get_next_query_run(schedule, base_datetime):
    return croniter(schedule, base_datetime).get_next(datetime)


def __now():
    return datetime.utcnow()
