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

import update_cluster


PROJECT_ID = os.environ['GCLOUD_PROJECT']
REGION = 'us-central1'
CLUSTER_NAME = 'test-cluster-{}'.format(str(uuid.uuid4()))
NUM_WORKERS = 2
NEW_WORKERS = NUM_WORKERS * 2


@pytest.fixture(autouse=True)
def setup_teardown():

    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(REGION)
    })

    cluster = {
        'project_id': PROJECT_ID,
        'cluster_name': CLUSTER_NAME,
        'config': {
            'master_config': {
                'num_instances': 1,
                'machine_type_uri': 'n1-standard-1'
            },
            'worker_config': {
                'num_instances': NUM_WORKERS,
                'machine_type_uri': 'n1-standard-1'
            }
        }
    }

    # Create the cluster
    operation = cluster_client.create_cluster(PROJECT_ID, REGION, cluster)
    operation.result()

    yield

    # Delete the cluster
    cluster_client.delete_cluster(PROJECT_ID, REGION, CLUSTER_NAME)


def test_update_cluster(capsys):
    # Wrapper function for client library function
    update_cluster.update_cluster(
        PROJECT_ID, REGION, CLUSTER_NAME, NEW_WORKERS
    )

    out, _ = capsys.readouterr()
    assert '{} workers'.format(NEW_WORKERS) in out
