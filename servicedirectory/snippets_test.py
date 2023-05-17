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

from _pytest.capture import CaptureFixture
import backoff
from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable
from google.cloud import servicedirectory_v1

import quickstart
import snippets

PROJECT_ID = environ["GOOGLE_CLOUD_PROJECT"]
LOCATION_ID = "us-east1"
NAMESPACE_ID = f"test-namespace-{uuid.uuid4().hex}"
SERVICE_ID = f"test-service-{uuid.uuid4().hex}"
ENDPOINT_ID = f"test-endpoint-{uuid.uuid4().hex}"
ADDRESS = "1.2.3.4"
PORT = 443


def teardown_module() -> None:
    client = servicedirectory_v1.RegistrationServiceClient()
    namespace_name = client.namespace_path(PROJECT_ID, LOCATION_ID, NAMESPACE_ID)
    all_namespaces = quickstart.list_namespaces(PROJECT_ID, LOCATION_ID).namespaces

    # Delete namespace only if it exists
    for namespace in all_namespaces:
        if namespace_name in namespace.name:
            try:
                client.delete_namespace(name=namespace_name)
            except NotFound:
                print("Namespace already deleted")
            break


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5
)
def test_create_namespace() -> None:
    response = snippets.create_namespace(PROJECT_ID, LOCATION_ID, NAMESPACE_ID)

    assert NAMESPACE_ID in response.name


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5
)
def test_create_service() -> None:
    response = snippets.create_service(
        PROJECT_ID, LOCATION_ID, NAMESPACE_ID, SERVICE_ID
    )

    assert SERVICE_ID in response.name


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5
)
def test_create_endpoint() -> None:
    response = snippets.create_endpoint(
        PROJECT_ID, LOCATION_ID, NAMESPACE_ID, SERVICE_ID, ENDPOINT_ID, ADDRESS, PORT
    )

    assert ENDPOINT_ID in response.name


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5
)
def test_resolve_service() -> None:
    response = snippets.resolve_service(
        PROJECT_ID, LOCATION_ID, NAMESPACE_ID, SERVICE_ID
    )

    assert len(response.service.endpoints) == 1
    assert ENDPOINT_ID in response.service.endpoints[0].name


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5
)
def test_delete_endpoint(capsys: CaptureFixture) -> None:
    snippets.delete_endpoint(
        PROJECT_ID, LOCATION_ID, NAMESPACE_ID, SERVICE_ID, ENDPOINT_ID
    )

    out, _ = capsys.readouterr()
    assert ENDPOINT_ID in out


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5
)
def test_delete_service(capsys: CaptureFixture) -> None:
    snippets.delete_service(PROJECT_ID, LOCATION_ID, NAMESPACE_ID, SERVICE_ID)

    out, _ = capsys.readouterr()
    assert SERVICE_ID in out


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5
)
def test_delete_namespace(capsys: CaptureFixture) -> None:
    snippets.delete_namespace(PROJECT_ID, LOCATION_ID, NAMESPACE_ID)

    out, _ = capsys.readouterr()
    assert NAMESPACE_ID in out
