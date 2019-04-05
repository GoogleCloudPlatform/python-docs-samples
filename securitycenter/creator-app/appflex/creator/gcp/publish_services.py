# pylint: disable=missing-docstring

import hashlib
from datetime import datetime, timezone

import os
import re
import jsonpickle
from google.api_core import exceptions
from google.cloud import pubsub
from google.oauth2 import service_account as sa

from creator.gcp import default_settings
from creator.config_service import (get_organization_display_name,
                                    get_organization_id, get_project_id)

DEFAULT_TOPIC = 'publish_processing'
TOPIC_PATTERN = 'projects/.+/topics/.+'
LOGGER = default_settings.configure_logger('publish_service')
PUBSUB_CREDENTIALS = os.getenv('PUBSUB_CREDENTIALS',
                               'accounts/publisher_sa.json')


def create_publisher(service_account):
    credentials = sa.Credentials.from_service_account_file(service_account)
    return pubsub.PublisherClient(credentials=credentials)


def verify_topic_existence(project, topic_path, publisher):
    project_path = publisher.project_path(project)

    topic_list = list(publisher.list_topics(project_path))
    if topic_path not in map(lambda x: x.name, topic_list):
        topic = publisher.create_topic(topic_path)
        LOGGER.debug('Topic created: {}'.format(topic))
    else:
        LOGGER.debug('Topic already exist')


def verify_project_id_in_topic_path(project, topic_path):
    project_pattern = 'projects/{}/topics/.+'.format(project)
    if re.fullmatch(project_pattern, topic_path):
        return project
    else:
        return re.search('projects/(.*)/topics/.+', topic_path).group(1)


def publish_result_to_topic(result, publisher, topic_path, kind, query):
    result_attributes = None
    if kind == 'ASSET':
        result.query = query
        result_hash = generate_result_hash(query['name'],
                                           result.name,
                                           result.state,
                                           result.updateTime)
        result_attributes = get_asset_metadata_fields(result, result_hash)
        result = jsonpickle.encode(result, unpicklable=False)
    elif kind == 'FINDING':
        result.query = query
        result_hash = generate_result_hash(query['name'],
                                           result.name,
                                           result.state,
                                           result.eventTime)
        result_attributes = get_finding_metadata_fields(result, result_hash)
        result = jsonpickle.encode(result, unpicklable=False)

    try:
        LOGGER.debug('result: %s', str(result))
        LOGGER.debug('result_attributes: %s', result_attributes)

        data = str(result)
        data = data.encode('utf-8')

        publisher.publish(topic_path, data, **result_attributes)
    except exceptions.NotFound as err:
        LOGGER.warning('Error trying to publish result data to topic %s, this message is not going to be processed again: %s', topic_path, err)


def generate_result_hash(*result_attributes):
    result_hash = ''
    for attr in result_attributes:
        result_hash += str(attr)
    return hashlib.md5(result_hash.encode()).hexdigest()


def get_asset_metadata_fields(asset, asset_hash):
    fields = {'Notification-Type': "ASSETS",
              'Organization-Id': str(get_organization_id()),
              'Organization-Display-Name': str(get_organization_display_name()),
              'Project-Id': str(get_project_asset_attr(asset)),
              'Count': "1",
              'Event-Type': str(asset.state),
              'Asset-Type': str(asset.securityCenterProperties['resourceType']),
              'Last-Updated-Time': str(asset.updateTime),
              'Asset-Id': str(asset.name),
              'Asset-Hash': str(asset_hash)}
    return fields


def get_finding_metadata_fields(source_finding, finding_hash):
    fields = {'Notification-Type': "FINDINGS",
              'Event-Type': str(source_finding.state),
              'Organization-Id': str(get_organization_id()),
              'Organization-Display-Name': str(get_organization_display_name()),
              'Project-Id': str(source_finding.name),
              'Count': "1",
              'Source-Id': str(source_finding.parent),
              'Asset-Id': str(source_finding.resourceName),
              'Category': str(source_finding.category),
              'Last-Updated-Time': str(source_finding.eventTime),
              'Finding-Id': str(source_finding.name),
              'Finding-Hash': str(finding_hash)}
    return fields


def get_project_asset_attr(asset):
    if asset.securityCenterProperties['resourceType'] == 'google.cloud.resourcemanager.Project':
        return asset.name
    elif asset.securityCenterProperties['resourceType'] == 'google.cloud.resourcemanager.Organization' or asset.securityCenterProperties['resourceType'] == 'google.cloud.resourcemanager.Folder':
        return None
    else:
        return asset.securityCenterProperties['resourceParent']


def __get_timestamp_in_utc(seconds):
    if seconds == 0:
        return ''
    return str(datetime.fromtimestamp(seconds, timezone.utc))


def publish_result(results, topic, kind, query):
    publisher = create_publisher(PUBSUB_CREDENTIALS)
    project_id = get_project_id()
    topic_name = topic if topic else DEFAULT_TOPIC
    if re.fullmatch(TOPIC_PATTERN, topic_name):
        topic_path = topic_name
    else:
        topic_path = publisher.topic_path(project_id, topic_name)

    project_id = verify_project_id_in_topic_path(project_id, topic_path)
    verify_topic_existence(project_id, topic_path, publisher)

    for result in results:
        publish_result_to_topic(result, publisher, topic_path, kind, query)
