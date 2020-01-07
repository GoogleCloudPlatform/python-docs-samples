# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid
import pytest

from google.cloud import dataproc_v1 as dataproc

import create_cluster

PROJECT_ID = os.environ['GCLOUD_PROJECT']
REGION = 'us-central1'
CLUSTER_NAME = 'test-cluster-{}'.format(str(uuid.uuid4()))


@pytest.fixture(autouse=True)
def teardown():
    yield

    client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(REGION)
    })
    # Client library function
    client.delete_cluster(PROJECT_ID, REGION, CLUSTER_NAME)


def test_cluster_create(capsys):
    # Wrapper function for client library function
    create_cluster.create_cluster(PROJECT_ID, REGION, CLUSTER_NAME)

    out, _ = capsys.readouterr()
    assert CLUSTER_NAME in out
