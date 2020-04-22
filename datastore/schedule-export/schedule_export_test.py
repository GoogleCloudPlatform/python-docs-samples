# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64

from unittest.mock import Mock

import main

mock_context = Mock()
mock_context.event_id = '617187464135194'
mock_context.timestamp = '2020-04-15T22:09:03.761Z'


def test_datastore_export(capsys):
    # Test an export without an entity filter
    bucket = 'gs://my-bucket'
    json_string = '{{ "bucket": "{bucket}" }}'.format(bucket=bucket)

    # Encode data like Cloud Scheduler
    data = bytes(json_string, 'utf-8')
    data_encoded = base64.b64encode(data)
    event = {"data": data_encoded}

    # Mock the Datastore service
    mockDatastore = Mock()
    main.datastore = mockDatastore

    # Call tested function
    main.datastore_export(event, mock_context)
    out, err = capsys.readouterr()
    export_args = mockDatastore.projects().export.call_args[1]
    req_body = export_args['body']
    # Assert request includes test values
    assert req_body['outputUrlPrefix'] == bucket


def test_datastore_export_entity_filter(capsys):
    # Test an export with an entity filter
    bucket = 'gs://my-bucket'
    kinds = 'Users,Tasks'
    namespaceIds = 'Customer831,Customer157'
    json_string = '{{ "bucket": "{bucket}", "kinds": "{kinds}", "namespaceIds": "{namespaceIds}" }}'.format(
        bucket=bucket, kinds=kinds, namespaceIds=namespaceIds)

    # Encode data like Cloud Scheduler
    data = bytes(json_string, 'utf-8')
    data_encoded = base64.b64encode(data)
    event = {"data": data_encoded}

    # Mock the Datastore service
    mockDatastore = Mock()
    main.datastore = mockDatastore

    # Call tested function
    main.datastore_export(event, mock_context)
    out, err = capsys.readouterr()
    export_args = mockDatastore.projects().export.call_args[1]
    req_body = export_args['body']
    # Assert request includes test values
    assert req_body['outputUrlPrefix'] == bucket
    assert req_body['entityFilter']['kinds'] == kinds
    assert req_body['entityFilter']['namespaceIds'] == namespaceIds
