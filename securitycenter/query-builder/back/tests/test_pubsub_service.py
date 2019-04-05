import uuid
import os
from unittest.mock import patch
import pytest

from client.scc_client_beta import Asset, Finding
from query_builder.domain_model.services.pubsub_service import (
    publish_queries_uuid,
    publish_result
)
import query_builder.application.default_settings as default_settings


ACCOUNT_SET = pytest.mark.skipif(
    not os.environ.get('NOTIFIER_CREDENTIALS', ''),
    not os.environ.get('PUBSUB_CREDENTIALS', ''),
    not os.environ.get('project_id', ''),
    not os.environ.get('organization_id', ''),
    reason='notifier and scheduler account not specified'
)


@ACCOUNT_SET
@patch('query_builder.application.default_settings.QUERIES_RUN_TOPIC',
       'projects/beta-qb-20181207132646/topics/Topic')
def test_publish_queries_uuid(mocker):
    # given
    _uuid = uuid.uuid4()
    uuids = [_uuid]
    with mocker.patch('google.api_core.grpc_helpers.create_channel'):
        with mocker.mock_module.patch(
                'google.cloud.pubsub_v1.PublisherClient.publish') as mock:
            # when
            publish_queries_uuid(uuids)
            # then
            mock.assert_called_with(default_settings.QUERIES_RUN_TOPIC,
                                    data=str(_uuid).encode())


@ACCOUNT_SET
def test_publish_result_with_asset_and_full_name_topic(mocker):
    # given
    owner = 'me@clsecteam.com'
    result_response = mock_result_response_with_asset()
    marks = {}
    actual_query = {}
    topic = 'projects/qb-test-local/topics/Topic'
    # given expected
    expected_topic_path = 'projects/qb-test-local/topics/Topic'
    expected_data = get_asset_result_data()
    expected_result_attributes = get_asset_result_attributes()

    with mocker.patch('google.api_core.grpc_helpers.create_channel'):
        with mocker.mock_module.patch(
                'google.cloud.pubsub_v1.PublisherClient.publish') as mock:
            # when
            publish_result(owner, result_response, marks, actual_query, topic)
            # then
            mock.assert_called_with(expected_topic_path,
                                    expected_data.encode('utf-8'),
                                    **expected_result_attributes)


@ACCOUNT_SET
def test_publish_result_with_finding_and_short_name_topic(mocker):
    # given
    owner = 'me@clsecteam.com'
    result_response = mock_result_response_with_finding()
    marks = {}
    actual_query = {}
    topic = 'Topic'
    # given expected
    expected_topic_path = 'projects/{}/topics/{}'.format(
        os.getenv('project_id'), topic)
    expected_data = get_finding_result_data()
    result_attributes = get_finding_result_attributes()

    with mocker.patch('google.api_core.grpc_helpers.create_channel'):
        with mocker.mock_module.patch(
                'google.cloud.pubsub_v1.PublisherClient.publish') as mock:
            # when
            publish_result(owner, result_response, marks, actual_query, topic)
            # then
            mock.assert_called_with(expected_topic_path,
                                    expected_data.encode('utf-8'),
                                    **result_attributes)


def get_asset_result_attributes():
    return {'Notification-Type': 'ASSETS', 'Organization-Id': '1055058000000',
            'Organization-Display-Name': 'None',
            'Project-Id': '//cloudresourcemanager.googleapis.com/projects/874894023622',
            'Count': '1', 'Event-Type': 'UNUSED',
            'Asset-Type': 'google.containerregistry.Image',
            'Last-Updated-Time': '2018-11-29T02:17:28.222Z',
            'Asset-Id': 'organizations/1055058000000/assets/15336941556789351944',
            'Asset-Hash': '2497c8906de9b2b3ea116625ae55a91f', 'Marks': '{}',
            'Additional_Dest_Email': 'me@clsecteam.com'}


def get_asset_result_data():
    return '{"createTime": "2018-11-29T02:17:28.222Z", "name": "organizations/1055058000000/assets/15336941556789351944", "query": {}, "resourceProperties": {"imageSizeBytes": "1225315912", "mediaType": "application/vnd.docker.distribution.manifest.v2+json", "name": "gcr.io/beta-cscc-api-clsecteam/jupyter-gcloud-cscc@sha256:54a2246c97e5fc9a44d59a6efb8a07f20f50aa6d4b1660a0943be8c97d6ab5ed", "tags": "[\\"v1\\"]", "timeUploaded": "2018-11-02t00:23:27.845597z"}, "securityCenterProperties": {"resourceName": "gcr.io/beta-cscc-api-clsecteam/jupyter-gcloud-cscc@sha256:54a2246c97e5fc9a44d59a6efb8a07f20f50aa6d4b1660a0943be8c97d6ab5ed", "resourceOwners": ["user:dan@ciandt.com"], "resourceParent": "//cloudresourcemanager.googleapis.com/projects/874894023622", "resourceProject": "//cloudresourcemanager.googleapis.com/projects/874894023622", "resourceType": "google.containerregistry.Image"}, "securityMarks": {"name": "organizations/1055058000000/assets/15336941556789351944/securityMarks"}, "state": "UNUSED", "updateTime": "2018-11-29T02:17:28.222Z"}'


def get_finding_result_attributes():
    return {'Notification-Type': 'FINDINGS',
            'Event-Type': 'ACTIVE',
            'Organization-Id': '1055058000000',
            'Organization-Display-Name': 'None',
            'Project-Id': 'organizations/1055058000000/sources/10711839371761827624/findings/u5gh9794guthg47940001',
            'Count': '1',
            'Source-Id': 'organizations/1055058000000/sources/10711839371761827624',
            'Asset-Id': 'organizations/1055058000000/assets/16712790543092542367',
            'Category': 'PROJECT_ACCESS',
            'Last-Updated-Time': '2018-10-30T12:27:43Z',
            'Finding-Id': 'organizations/1055058000000/sources/10711839371761827624/findings/u5gh9794guthg47940001',
            'Finding-Hash': '29e956361ce1bf4c6c0c897df5083d22',
            'Marks': '{}',
            'Additional_Dest_Email': 'me@clsecteam.com'}


def get_finding_result_data():
    return '{"category": "PROJECT_ACCESS", "createTime": "2018-10-30T12:27:43Z", "eventTime": "2018-10-30T12:27:43Z", "externalUri": ' \
           '"https://console.cloud.google.com", "name": "organizations/1055058000000/sources/10711839371761827624/findings/u5gh9794guthg47940001", ' \
           '"parent": "organizations/1055058000000/sources/10711839371761827624", ' \
           '"query": {}, "resourceName": "organizations/1055058000000/assets/16712790543092542367", ' \
           '"securityMarks": {"marks": {"beta-api": "value2", "beta_api": "value1", "not_demo": "true", "scc_beta_client_test": "test_mark", "scc_query_test74b8f5a8-1234-50fb-9acc-6377ecf5159b": "working_test74b8f5a8-1234-50fb-9acc-6377ecf5159b"}, "name": "organizations/1055058000000/sources/10711839371761827624/findings/u5gh9794guthg47940001/securityMarks"}, ' \
           '"sourceProperties": {"scc_environment": "hackathon"}, "state": "ACTIVE"}'


def mock_result_response_with_asset():
    asset = {
        "name": "organizations/1055058000000/assets/15336941556789351944",
        "securityCenterProperties": {
            "resourceName": "gcr.io/beta-cscc-api-clsecteam/jupyter-gcloud-cscc@sha256:54a2246c97e5fc9a44d59a6efb8a07f20f50aa6d4b1660a0943be8c97d6ab5ed",
            "resourceType": "google.containerregistry.Image",
            "resourceParent": "//cloudresourcemanager.googleapis.com/projects/874894023622",
            "resourceProject": "//cloudresourcemanager.googleapis.com/projects/874894023622",
            "resourceOwners": [
                "user:dan@ciandt.com"
            ]
        },
        "resourceProperties": {
            "imageSizeBytes": "1225315912",
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "name": "gcr.io/beta-cscc-api-clsecteam/jupyter-gcloud-cscc@sha256:54a2246c97e5fc9a44d59a6efb8a07f20f50aa6d4b1660a0943be8c97d6ab5ed",
            "tags": "[\"v1\"]",
            "timeUploaded": "2018-11-02t00:23:27.845597z"
        },
        "securityMarks": {
            "name": "organizations/1055058000000/assets/15336941556789351944/securityMarks"
        },
        "createTime": "2018-11-29T02:17:28.222Z",
        "updateTime": "2018-11-29T02:17:28.222Z"
    }
    asset = Asset(asset, state="UNUSED")
    result_response = {
        "ASSET": [asset],
        "FINDING": []
    }
    return result_response


def mock_result_response_with_finding():
    finding = {
        "name": "organizations/1055058000000/sources/10711839371761827624/findings/u5gh9794guthg47940001",
        "parent": "organizations/1055058000000/sources/10711839371761827624",
        "resourceName": "organizations/1055058000000/assets/16712790543092542367",
        "state": "ACTIVE",
        "category": "PROJECT_ACCESS",
        "externalUri": "https://console.cloud.google.com",
        "sourceProperties": {
            "scc_environment": "hackathon"
        },
        "securityMarks": {
            "name": "organizations/1055058000000/sources/10711839371761827624/findings/u5gh9794guthg47940001/securityMarks",
            "marks": {
                "beta_api": "value1",
                "scc_query_test74b8f5a8-1234-50fb-9acc-6377ecf5159b": "working_test74b8f5a8-1234-50fb-9acc-6377ecf5159b",
                "beta-api": "value2",
                "scc_beta_client_test": "test_mark",
                "not_demo": "true"
            }
        },
        "eventTime": "2018-10-30T12:27:43Z",
        "createTime": "2018-10-30T12:27:43Z"
    }
    finding = Finding(finding)

    result_response = {
        "ASSET": [],
        "FINDING": [finding]
    }
    return result_response
