import os
import json
import re

from google.oauth2 import service_account as sa
from google.cloud import pubsub

import query_builder.application.default_settings as default_settings
from .configuration_service import (
    is_production_environment,
    get_default_notification_topic,
    get_project_id
)

from ..helpers.parse_results import get_asset_result, get_finding_result

LOGGER = default_settings.configure_logger('pubsub_service')

FINDING_KIND = 'FINDING'
ASSET_KIND = 'ASSET'
TOPIC_PATTERN = 'projects/.+/topics/.+'


def publish_queries_uuid(uuids):
    """Publishes the queries uuid passed on topic to be executed asynchronously"""
    topic_path = default_settings.QUERIES_RUN_TOPIC
    if not topic_path:
        LOGGER.error(
            'Topic not specified, queries uuid %s can not be published.', uuids)
        return

    LOGGER.info(
        'Publishing queries uuid to run: %s on topic: %s',
        uuids, topic_path)
    client = __get_publisher_client('PUBSUB_CREDENTIALS')
    for uuid in uuids:
        client.publish(topic_path,
                       data=str(uuid).encode())


def publish_uuid_to_clean(uuid):
    """Publishes the query uuid passed on to topic to be cleaned asynchronously"""
    if not is_production_environment():
        LOGGER.info('clean up active only on production env.')
        return

    topic_path = default_settings.MARK_CLEAN_UP_TOPIC
    if not topic_path:
        LOGGER.error(
            'Topic not specified, uuid %s to be clean up can not be published.',
            uuid
        )
        return

    LOGGER.info(
        'Publishing uuid to be clean up: %s on topic: %s',
        uuid,
        topic_path
    )
    client = __get_publisher_client('PUBSUB_CREDENTIALS')
    client.publish(topic_path, data=str(uuid).encode())


def publish_result(owner, result_response, marks, actual_query, topic=None):
    """Publishes assets and findings returned from scc to a notifier topic
    :param owner: the email of the person who saved the query
    :param result_response: the response from the scc-client by kind
    :param marks: a string with the marks separated by comma
    :param actual_query: a dict with the query parameters
    :param topic: the name of the topic where the results will be published
    """
    publisher = __get_publisher_client('NOTIFIER_CREDENTIALS')
    assets = result_response[ASSET_KIND]
    findings = result_response[FINDING_KIND]
    topic = topic if topic else get_default_notification_topic()

    if re.fullmatch(TOPIC_PATTERN, topic):
        topic_path = topic
    else:
        topic_path = publisher.topic_path(get_project_id(), topic)
    for asset in assets:
        __publish_result_to_topic(publisher,
                                  owner, asset,
                                  marks, topic_path,
                                  'ASSET', actual_query)

    for finding in findings:
        __publish_result_to_topic(publisher,
                                  owner, finding,
                                  marks, topic_path,
                                  'FINDING', actual_query)


def __get_publisher_client(service_account_name):
    sa_json = os.getenv(service_account_name)
    credentials = sa.Credentials.from_service_account_info(json.loads(sa_json))
    return pubsub.PublisherClient(credentials=credentials)


def __publish_result_to_topic(publisher, owner, result, marks,
                              topic, kind, actual_query):
    result_attributes = None
    if kind == 'ASSET':
        result, result_attributes = get_asset_result(owner,
                                                     result,
                                                     marks,
                                                     actual_query)
    elif kind == 'FINDING':
        result, result_attributes = get_finding_result(owner,
                                                       result,
                                                       marks,
                                                       actual_query)
    LOGGER.debug(str(result))
    LOGGER.debug(result_attributes)
    data = str(result)

    data = data.encode('utf-8')
    publisher.publish(topic, data, **result_attributes)
