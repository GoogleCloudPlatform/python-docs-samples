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

from dataclasses import dataclass
import itertools
import json
import multiprocessing as mp
import os
import subprocess
import sys
import time
from typing import Any, Callable, Dict, Iterable, Optional
import uuid

import pytest

# Default options.
UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-west1"
ZONE = "us-west1-b"

RETRY_MAX_TIME = 5 * 60  # 5 minutes in seconds


@dataclass
class Utils:
    uuid: str = UUID
    project: str = PROJECT
    region: str = REGION
    zone: str = ZONE

    @staticmethod
    def storage_bucket(bucket_name: str) -> str:
        from google.cloud import storage

        storage_client = storage.Client()
        bucket_unique_name = f"{bucket_name}-{UUID}"
        bucket = storage_client.create_bucket(bucket_unique_name)

        print(f"storage_bucket: {bucket_unique_name}")
        yield bucket_unique_name

        bucket.delete(force=True)

    @staticmethod
    def bigquery_dataset(dataset_name: str, project: str = PROJECT) -> str:
        from google.cloud import bigquery

        bigquery_client = bigquery.Client()
        dataset = bigquery_client.create_dataset(
            bigquery.Dataset(f"{project}.{dataset_name.replace('-', '_')}_{UUID}")
        )

        print(f"bigquery_dataset: {dataset.full_dataset_id}")
        yield dataset.full_dataset_id

        bigquery_client.delete_dataset(
            dataset.full_dataset_id.replace(":", "."), delete_contents=True
        )

    @staticmethod
    def bigquery_query(query: str) -> Iterable[Dict[str, Any]]:
        from google.cloud import bigquery

        bigquery_client = bigquery.Client()
        for row in bigquery_client.query(query):
            yield dict(row)

    @staticmethod
    def pubsub_topic(topic_name: str, project: str = PROJECT) -> str:
        from google.cloud import pubsub

        publisher_client = pubsub.PublisherClient()
        topic_path = publisher_client.topic_path(project, f"{topic_name}-{UUID}")
        topic = publisher_client.create_topic(topic_path)

        print(f"pubsub_topic: {topic.name}")
        yield topic.name

        # Due to the pinned library dependencies in apache-beam, client
        # library throws an error upon deletion.
        # We use gcloud for a workaround. See also:
        # https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4492
        cmd = ["gcloud", "pubsub", "--project", project, "topics", "delete", topic.name]
        print(cmd)
        subprocess.run(cmd, check=True)

    @staticmethod
    def pubsub_subscription(
        topic_path: str,
        subscription_name: str,
        project: str = PROJECT,
    ) -> str:
        from google.cloud import pubsub

        subscriber = pubsub.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            project, f"{subscription_name}-{UUID}"
        )
        subscription = subscriber.create_subscription(subscription_path, topic_path)

        print(f"pubsub_subscription: {subscription.name}")
        yield subscription.name

        # Due to the pinned library dependencies in apache-beam, client
        # library throws an error upon deletion.
        # We use gcloud for a workaround. See also:
        # https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4492
        cmd = [
            "gcloud",
            "pubsub",
            "--project",
            project,
            "subscriptions",
            "delete",
            subscription.name,
        ]
        print(cmd)
        subprocess.run(cmd, check=True)

    @staticmethod
    def pubsub_publisher(
        topic_path: str,
        new_msg: Callable[[int], str] = lambda i: json.dumps(
            {"id": i, "content": f"message {i}"}
        ),
        sleep_sec: int = 1,
    ) -> bool:
        from google.cloud import pubsub

        def _infinite_publish_job() -> None:
            publisher_client = pubsub.PublisherClient()
            for i in itertools.count():
                msg = new_msg(i)
                publisher_client.publish(topic_path, msg.encode("utf-8")).result()
                time.sleep(sleep_sec)

        # Start a subprocess in the background to do the publishing.
        print(f"Starting publisher on {topic_path}")
        p = mp.Process(target=_infinite_publish_job)
        p.start()

        yield p.is_alive()

        # For cleanup, terminate the background process.
        print("Stopping publisher")
        p.join(timeout=0)
        p.terminate()

    @staticmethod
    def container_image(
        image_path: str,
        project: str = PROJECT,
        tag: str = "latest",
    ) -> str:
        image_name = f"gcr.io/{project}/{image_path}-{UUID}:{tag}"
        cmd = ["gcloud", "auth", "configure-docker"]
        print(cmd)
        subprocess.run(cmd, check=True)
        cmd = [
            "gcloud",
            "builds",
            "submit",
            f"--project={project}",
            f"--tag={image_name}",
            ".",
        ]
        print(cmd)
        subprocess.run(cmd, check=True)

        print(f"container_image: {image_name}")
        yield image_name

        cmd = [
            "gcloud",
            "container",
            "images",
            "delete",
            image_name,
            f"--project={project}",
            "--quiet",
        ]
        print(cmd)
        subprocess.run(cmd, check=True)

    @staticmethod
    def dataflow_job_id_from_job_name(
        job_name: str,
        project: str = PROJECT,
    ) -> Optional[str]:
        from googleapiclient.discovery import build

        dataflow = build("dataflow", "v1b3")

        # Only return the 50 most recent results - our job is likely to be in here.
        # If the job is not found, first try increasing this number.[]''job_id
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

    @staticmethod
    def dataflow_jobs_wait(
        job_id: str,
        project: str = PROJECT,
        status: str = "JOB_STATE_RUNNING",
    ) -> bool:
        from googleapiclient.discovery import build

        dataflow = build("dataflow", "v1b3")

        sleep_time_seconds = 30
        max_sleep_time = 10 * 60

        print(f"Waiting for Dataflow job ID: {job_id} (until status {status})")
        for _ in range(0, max_sleep_time, sleep_time_seconds):
            try:
                # For more info see:
                #   https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/get
                jobs_request = (
                    dataflow.projects()
                    .jobs()
                    .get(
                        projectId=project,
                        jobId=job_id,
                        view="JOB_VIEW_SUMMARY",
                    )
                )
                response = jobs_request.execute()
                print(response)
                if response["currentState"] == status:
                    return True
            except:
                pass
            time.sleep(sleep_time_seconds)
        return False

    @staticmethod
    def dataflow_jobs_cancel_by_job_id(
        job_id: str, project: str = PROJECT, region: str = REGION
    ) -> None:
        print(f"Canceling Dataflow job ID: {job_id}")
        # We get an error using the googleapiclient.discovery APIs, probably
        # due to incompatible dependencies with apache-beam.
        # We use gcloud instead to cancel the job.
        #   https://cloud.google.com/sdk/gcloud/reference/dataflow/jobs/cancel
        cmd = [
            "gcloud",
            f"--project={project}",
            "dataflow",
            "jobs",
            "cancel",
            job_id,
            f"--region={region}",
        ]
        subprocess.run(cmd, check=True)

    @staticmethod
    def dataflow_jobs_cancel_by_job_name(
        job_name: str, project: str = PROJECT, region: str = REGION
    ) -> None:
        # To cancel a dataflow job, we need its ID, not its name.
        # If it doesn't, job_id will be equal to None.
        job_id = Utils.dataflow_job_id_from_job_name(project, job_name)
        if job_id is not None:
            Utils.dataflow_jobs_cancel_by_job_id(job_id, project, region)

    @staticmethod
    def dataflow_flex_template_build(
        bucket_name: str,
        template_image: str,
        metadata_file: str,
        project: str = PROJECT,
        template_file: str = "template.json",
    ) -> str:
        # https://cloud.google.com/sdk/gcloud/reference/dataflow/flex-template/build
        template_gcs_path = f"gs://{bucket_name}/{template_file}"
        cmd = [
            "gcloud",
            "dataflow",
            "flex-template",
            "build",
            template_gcs_path,
            f"--project={project}",
            f"--image={template_image}",
            "--sdk-language=PYTHON",
            f"--metadata-file={metadata_file}",
        ]
        print(cmd)
        subprocess.run(cmd, check=True)

        print(f"dataflow_flex_template_build: {template_gcs_path}")
        yield template_gcs_path
        # The template file gets deleted when we delete the bucket.

    @staticmethod
    def dataflow_flex_template_run(
        job_name: str,
        template_path: str,
        bucket_name: str,
        parameters: Dict[str, str] = {},
        project: str = PROJECT,
        region: str = REGION,
    ) -> str:
        import yaml

        # https://cloud.google.com/sdk/gcloud/reference/dataflow/flex-template/run
        unique_job_name = f"{job_name}-{UUID}"
        print(f"dataflow_job_name: {unique_job_name}")
        cmd = [
            "gcloud",
            "dataflow",
            "flex-template",
            "run",
            unique_job_name,
            f"--template-file-gcs-location={template_path}",
            f"--project={project}",
            f"--region={region}",
        ] + [
            f"--parameters={name}={value}"
            for name, value in {
                **parameters,
                "temp_location": f"gs://{bucket_name}/temp",
            }.items()
        ]
        print(cmd)
        try:
            # The `capture_output` option was added in Python 3.7, so we must
            # pass the `stdout` and `stderr` options explicitly to support 3.6.
            # https://docs.python.org/3/library/subprocess.html#subprocess.run
            p = subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout = p.stdout.decode("utf-8")
            stderr = p.stderr.decode("utf-8")
            print(f"Launched Dataflow Flex Template job: {unique_job_name}")
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)
            stdout = stdout.decode("utf-8")
            stderr = stderr.decode("utf-8")
        finally:
            print("--- stderr ---")
            print(stderr)
            print("--- stdout ---")
            print(stdout)
            print("--- end ---")
        return yaml.safe_load(stdout)["job"]["id"]


@pytest.fixture(scope="session")
def utils() -> Utils:
    print(f"Test unique identifier: {UUID}")
    subprocess.run(["gcloud", "version"])
    return Utils()
