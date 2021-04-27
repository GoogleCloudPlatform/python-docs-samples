# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from datetime import time
import itertools
import json
import multiprocessing as mp
import os
import subprocess
from typing import Callable, Dict, Optional
import uuid

import backoff
from google.cloud import bigquery
from google.cloud import pubsub
from google.cloud import storage
from google.cloud.bigquery.table import RowIterator
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

dataflow = build("dataflow", "v1b3")

# Default options.
UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-west1"
ZONE = "us-west1-b"

RETRY_MAX_TIME = 5 * 60  # 5 minutes in seconds


def storage_bucket(bucket_name: str) -> str:
    storage_client = storage.Client()
    bucket_unique_name = f"{bucket_name}-{UUID}"
    bucket = storage_client.create_bucket(bucket_unique_name)

    print(f"storage_bucket: {repr(bucket_unique_name)}")
    yield bucket_unique_name

    bucket.delete(force=True)


def bigquery_dataset(dataset_name: str, project: str = PROJECT) -> str:
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.create_dataset(
        bigquery.Dataset(f"{project}.{dataset_name}_{UUID}")
    )

    print(f"bigquery_dataset: {dataset.full_dataset_id}")
    yield dataset.full_dataset_id

    bigquery_client.delete_dataset(dataset.full_dataset_id, delete_contents=True)


def bigquery_query(query: str) -> RowIterator:
    bigquery_client = bigquery.Client()
    query_job = bigquery_client.query(query)
    return query_job.result()


def pubsub_topic(topic_name: str, project: str = PROJECT) -> str:
    publisher_client = pubsub.PublisherClient()
    topic_path = publisher_client.topic_path(project, f"{topic_name}-{UUID}")
    topic = publisher_client.create_topic(topic_path)

    print(f"pubsub_topic: {repr(topic.name)}")
    yield topic.name

    # Due to the pinned library dependencies in apache-beam, client
    # library throws an error upon deletion.
    # We use gcloud for a workaround. See also:
    # https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4492
    subprocess.check_call(
        ["gcloud", "pubsub", "--project", project, "topics", "delete", topic],
        check=True,
    )


def pubsub_subscription(
    topic_path: str, subscription_name: str, project: str = PROJECT
) -> str:
    subscriber = pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, f"{subscription_name}-{UUID}"
    )
    subscription = subscriber.create_subscription(subscription_path, topic_path)

    print(f"pubsub_subscription: {repr(subscription.name)}")
    yield subscription.name

    # Due to the pinned library dependencies in apache-beam, client
    # library throws an error upon deletion.
    # We use gcloud for a workaround. See also:
    # https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4492
    subprocess.check_call(
        [
            "gcloud",
            "pubsub",
            "--project",
            project,
            "subscriptions",
            "delete",
            subscription_name,
        ],
        check=True,
    )


def pubsub_publisher(
    topic_path: str,
    new_msg: Callable[[int], str] = lambda i: json.dumps(
        {"id": i, "content": f"message {i}"}
    ),
) -> bool:
    def _infinite_publish_job() -> None:
        publisher_client = pubsub.PublisherClient()
        for i in itertools.count():
            publisher_client.publish(topic_path, new_msg(i).encode("utf-8")).result()
            time.sleep(1)

    # Start a subprocess in the background to do the publishing.
    p = mp.Process(target=_infinite_publish_job)
    p.start()

    yield p.is_alive()

    # For cleanup, terminate the background process.
    p.join(timeout=0)
    p.terminate()


def container_image(
    image_path: str,
    project: str = PROJECT,
    tag: str = "latest",
) -> str:
    image_name = f"gcr.io/{project}/{image_path}-{UUID}:{tag}"
    subprocess.run(["gcloud", "auth", "configure-docker"], check=True)
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            f"--project={project}",
            f"--tag={image_name}",
            ".",
        ],
        check=True,
    )

    yield image_name

    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            image_name,
            f"--project={project}",
            "--quiet",
        ],
        check=True,
    )


def dataflow_job_id_from_job_name(
    job_name: str, project: str = PROJECT
) -> Optional[str]:
    # Only return the 50 most recent results - our job is likely to be in here.
    # If the job is not found, first try increasing this number.
    # For more info see:
    #   https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/list
    jobs_request = (
        dataflow.projects()
        .jobs()
        .list(
            projectId=project,
            filter="ACTIVE",
            pageSize=50,
        )
    )
    response = jobs_request.execute()

    # Search for the job in the list that has our name (names are unique)
    for job in response["jobs"]:
        if job["name"] == job_name:
            return job["id"]
    return None


@backoff.on_exception(backoff.expo, HttpError, max_time=RETRY_MAX_TIME)
def dataflow_jobs_cancel(job_name: str, project: str = PROJECT) -> None:
    # To cancel a dataflow job, we need its ID, not its name
    job_id = dataflow_job_id_from_job_name(project, job_name)

    if job_id is not None:
        # Cancel the Dataflow job if it exists.
        # If it doesn't, job_id will be equal to None.
        # For more info, see:
        #   https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/update
        request = (
            dataflow.projects()
            .jobs()
            .update(
                projectId=project,
                jobId=job_id,
                body={"requestedState": "JOB_STATE_CANCELLED"},
            )
        )
        request.execute()


@staticmethod
def dataflow_flex_template_build(
    bucket_name: str,
    template_image: str,
    metadata_file: str,
    project: str = PROJECT,
    template_file: str = "template.json",
) -> str:
    subprocess.call(
        [
            "gcloud",
            "dataflow",
            "flex-template",
            "build",
            f"gs://{bucket_name}/{template_file}",
            f"--project={project}",
            f"--image={template_image}",
            "--sdk-language=PYTHON",
            f"--metadata-file={metadata_file}",
        ],
        check=True,
    )

    yield f"gs://{bucket_name}/{template_file}"

    storage_client = storage.Client()
    storage_client.bucket(bucket_name).blob(template_file).delete()


def dataflow_flex_template_run(
    job_name: str,
    template_path: str,
    bucket_name: str,
    parameters: Dict[str, str] = {},
    project: str = PROJECT,
    region: str = REGION,
) -> str:
    unique_job_name = f"{job_name}-{UUID}"
    subprocess.call(
        [
            "gcloud",
            "dataflow",
            "flex-template",
            "run",
            unique_job_name,
            f"--template-file-gcs-location={template_path}",
            f"--project={project}",
            f"--region={region}",
            f"--temp_location=gs://{bucket_name}/temp",
        ]
        + [f"--parameters={name}={value}" for name, value in parameters.items()],
        check=True,
    )

    yield unique_job_name
