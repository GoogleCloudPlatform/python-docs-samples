#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
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

from os import environ
import uuid

from google.api_core import exceptions
from google.cloud import servicedirectory_v1

import snippets

PROJECT_ID = environ['GOOGLE_CLOUD_PROJECT']
LOCATION_ID = 'us-east1'
NAMESPACE_ID = f'test-namespace-{uuid.uuid4().hex}'
SERVICE_ID = f'test-service-{uuid.uuid4().hex}'
ENDPOINT_ID = f'test-endpoint-{uuid.uuid4().hex}'
ADDRESS = '1.2.3.4'
PORT = 443


def teardown_module():
    client = servicedirectory_v1.RegistrationServiceClient()
    namespace_name = client.namespace_path(PROJECT_ID, LOCATION_ID, NAMESPACE_ID)
    try:
        namespace = client.get_namespace(name=namespace_name)
        client.delete_namespace(name=namespace.name)
    except exceptions.NotFound:
        pass


def test_create_namespace():
    response = snippets.create_namespace(PROJECT_ID, LOCATION_ID, NAMESPACE_ID)

    assert NAMESPACE_ID in response.name


def test_create_service():
    response = snippets.create_service(PROJECT_ID, LOCATION_ID, NAMESPACE_ID,
                                       SERVICE_ID)

    assert SERVICE_ID in response.name


def test_create_endpoint():
    response = snippets.create_endpoint(PROJECT_ID, LOCATION_ID, NAMESPACE_ID,
                                        SERVICE_ID, ENDPOINT_ID, ADDRESS, PORT)

    assert ENDPOINT_ID in response.name


def test_resolve_service():
    response = snippets.resolve_service(PROJECT_ID, LOCATION_ID, NAMESPACE_ID,
                                        SERVICE_ID)

    assert len(response.service.endpoints) == 1
    assert ENDPOINT_ID in response.service.endpoints[0].name


def test_delete_endpoint(capsys):
    snippets.delete_endpoint(PROJECT_ID, LOCATION_ID, NAMESPACE_ID, SERVICE_ID,
                             ENDPOINT_ID)

    out, _ = capsys.readouterr()
    assert ENDPOINT_ID in out


def test_delete_service(capsys):
    snippets.delete_service(PROJECT_ID, LOCATION_ID, NAMESPACE_ID, SERVICE_ID)

    out, _ = capsys.readouterr()
    assert SERVICE_ID in out


def test_delete_namespace(capsys):
    snippets.delete_namespace(PROJECT_ID, LOCATION_ID, NAMESPACE_ID)

    out, _ = capsys.readouterr()
    assert NAMESPACE_ID in out
