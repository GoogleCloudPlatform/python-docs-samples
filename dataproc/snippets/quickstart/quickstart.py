#!/usr/bin/env python

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

# [START dataproc_quickstart]
"""
This quickstart sample walks a user through creating a Cloud Dataproc
cluster, submitting a PySpark job from Google Cloud Storage to the
cluster, reading the output of the job and deleting the cluster, all
using the Python client library.

Usage:
    python quickstart.py --project_id <PROJECT_ID> --region <REGION> \
        --cluster_name <CLUSTER_NAME> --job_file_path <GCS_JOB_FILE_PATH>
"""

import argparse
import time

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage


def quickstart(project_id, region, cluster_name, job_file_path):
    # Create the cluster client.
    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    # Create the cluster config.
    cluster = {
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

    # Create the cluster.
    operation = cluster_client.create_cluster(project_id, region, cluster)
    result = operation.result()

    print('Cluster created successfully: {}'.format(result.cluster_name))

    # Create the job client.
    job_client = dataproc.JobControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    # Create the job config.
    job = {
        'placement': {
            'cluster_name': cluster_name
        },
        'pyspark_job': {
            'main_python_file_uri': job_file_path
        }
    }

    job_response = job_client.submit_job(project_id, region, job)
    job_id = job_response.reference.job_id

    print('Submitted job \"{}\".'.format(job_id))

    # Termimal states for a job.
    terminal_states = {
        dataproc.types.JobStatus.ERROR,
        dataproc.types.JobStatus.CANCELLED,
        dataproc.types.JobStatus.DONE
    }

    # Create a timeout such that the job gets cancelled if not in a
    # terminal state after a fixed period of time.
    timeout_seconds = 600
    time_start = time.time()

    # Wait for the job to complete.
    while job_response.status.state not in terminal_states:
        if time.time() > time_start + timeout_seconds:
            job_client.cancel_job(project_id, region, job_id)
            print('Job {} timed out after threshold of {} seconds.'.format(
                job_id, timeout_seconds))

        # Poll for job termination once a second.
        time.sleep(1)
        job_response = job_client.get_job(project_id, region, job_id)

    # Cloud Dataproc job output gets saved to a GCS bucket allocated to it.
    cluster_info = cluster_client.get_cluster(
        project_id, region, cluster_name)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(cluster_info.config.config_bucket)
    output_blob = (
        'google-cloud-dataproc-metainfo/{}/jobs/{}/driveroutput.000000000'
        .format(cluster_info.cluster_uuid, job_id))
    output = bucket.blob(output_blob).download_as_string()

    print('Job {} finished with state {}:\n{}'.format(
        job_id,
        job_response.status.State.Name(job_response.status.state),
        output))

    # Delete the cluster once the job has terminated.
    operation = cluster_client.delete_cluster(project_id, region, cluster_name)
    operation.result()

    print('Cluster {} successfully deleted.'.format(cluster_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--project_id',
        type=str,
        required=True,
        help='Project to use for creating resources.')
    parser.add_argument(
        '--region',
        type=str,
        required=True,
        help='Region where the resources should live.')
    parser.add_argument(
        '--cluster_name',
        type=str,
        required=True,
        help='Name to use for creating a cluster.')
    parser.add_argument(
        '--job_file_path',
        type=str,
        required=True,
        help='Job in GCS to execute against the cluster.')

    args = parser.parse_args()
    quickstart(args.project_id, args.region,
               args.cluster_name, args.job_file_path)
# [END dataproc_quickstart]
