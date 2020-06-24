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
import pytest
import quickstart
from google.api_core import exceptions
from google.cloud import servicedirectory_v1beta1

PROJECT_ID = environ['GOOGLE_CLOUD_PROJECT']
LOCATION_ID = 'us-east1'
NAMESPACE_ID = 'test-namespace'


@pytest.fixture(scope='module')
def client():
  return servicedirectory_v1beta1.RegistrationServiceClient()


@pytest.fixture(scope='module')
def namespace(client):
  return servicedirectory_v1beta1.Namespace(
      name=client.namespace_path(PROJECT_ID, LOCATION_ID, NAMESPACE_ID))


@pytest.fixture(scope='module')
def list_namespace(client, namespace):
  created = False
  try:
    client.get_namespace(name=namespace.name)
  except exceptions.NotFound as e:
    client.create_namespace(
        parent='projects/{0}/locations/{1}'.format(PROJECT_ID, LOCATION_ID),
        namespace=namespace,
        namespace_id=NAMESPACE_ID,
    )
    created = True

  yield quickstart.list_namespaces(PROJECT_ID, LOCATION_ID)

  if created:
    client.delete_namespace(name=namespace.name)


def test_list_namespace(namespace, list_namespace):
  assert namespace in list_namespace.namespaces
