import os, uuid
import pytest
import setup

from google.cloud import dataproc_v1 as dataproc


PROJECT_ID = os.environ("GCLOUD_PROJECT")
REGION = "us-central1"

def test_dirty_data():
    # create cluster client
    client = dataproc.ClusterControllerClient(client_options={
            "api_endpoint": "{}-dataproc.googleapis.com:443".format(REGION),
        })
    
    cluster_config = {
            'project_id': project_id,
            'cluster_name': cluster_name,
            'config': {
                'master_config': {
                    'num_instances': 1,
                    'machine_type_uri': 'n1-standard-1'
                    },
                'worker_config': {
                    'num_instances': 2,
                    'machine_type_uri': 'n1-standard-1'
                    }
                }
            }

    operation = client.create_cluster(PROJECT_ID, REGION, cluster_config)

    result = operation.result()

    print("Cluster created successfully")

