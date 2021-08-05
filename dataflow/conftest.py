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
import logging
import multiprocessing as mp
import os
import platform
import re
import subprocess
import sys
import time
from typing import Any, Callable, Dict, Iterable, Optional
import uuid

import pytest

# Default options.
UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"

TIMEOUT_SEC = 30 * 60  # 30 minutes in seconds
POLL_INTERVAL_SEC = 60  # 1 minute in seconds

HYPHEN_NAME_RE = re.compile(r"[^\w\d-]+")
UNDERSCORE_NAME_RE = re.compile(r"[^\w\d_]+")

PYTHON_VERSION = "".join(platform.python_version_tuple()[0:2])


@dataclass
class Utils:
    uuid: str = UUID
    project: str = PROJECT
    region: str = REGION

    @staticmethod
    def hyphen_name(name: str) -> str:
        unique_name = f"{name}-py{PYTHON_VERSION}-{UUID}"
        return HYPHEN_NAME_RE.sub("-", unique_name)

    @staticmethod
    def underscore_name(name: str) -> str:
        return UNDERSCORE_NAME_RE.sub("_", Utils.hyphen_name(name))

    @staticmethod
    def storage_bucket(name: str) -> str:
        from google.cloud import storage

        storage_client = storage.Client()
        bucket = storage_client.create_bucket(Utils.hyphen_name(name))

        logging.info(f"Created storage_bucket: {bucket.name}")
        yield bucket.name

        # Print all the objects in the bucket before deleting for debugging.
        logging.info(f"Deleting bucket {bucket.name} with the following contents:")
        total_files = 0
        total_size = 0
        for blob in bucket.list_blobs():
            logging.info(f"  - {blob.name} ({blob.size} bytes)")
            total_files += 1
            total_size += blob.size
        logging.info(f"Total {total_files} files ({total_size} bytes)")

        bucket.delete(force=True)
        logging.info(f"Deleted storage_bucket: {bucket.name}")

    @staticmethod
    def bigquery_dataset(name: str, project: str = PROJECT) -> str:
        from google.cloud import bigquery

        bigquery_client = bigquery.Client()

        dataset = bigquery_client.create_dataset(
            bigquery.Dataset(f"{project}.{Utils.underscore_name(name)}")
        )

        logging.info(f"Created bigquery_dataset: {dataset.full_dataset_id}")
        yield dataset.full_dataset_id

        bigquery_client.delete_dataset(
            dataset.full_dataset_id.replace(":", "."), delete_contents=True
        )
        logging.info(f"Deleted bigquery_dataset: {dataset.full_dataset_id}")

    @staticmethod
    def bigquery_query(query: str) -> Iterable[Dict[str, Any]]:
        from google.cloud import bigquery

        bigquery_client = bigquery.Client()
        logging.info(f"Bigquery query: {query}")
        for row in bigquery_client.query(query):
            yield dict(row)

    @staticmethod
    def pubsub_topic(name: str, project: str = PROJECT) -> str:
        from google.cloud import pubsub

        publisher_client = pubsub.PublisherClient()
        topic_path = publisher_client.topic_path(project, Utils.hyphen_name(name))
        topic = publisher_client.create_topic(topic_path)

        logging.info(f"Created pubsub_topic: {topic.name}")
        yield topic.name

        # Due to the pinned library dependencies in apache-beam, client
        # library throws an error upon deletion.
        # We use gcloud for a workaround. See also:
        # https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4492
        cmd = ["gcloud", "pubsub", "--project", project, "topics", "delete", topic.name]
        logging.info(f"{cmd}")
        subprocess.run(cmd, check=True)
        logging.info(f"Deleted pubsub_topic: {topic.name}")

    @staticmethod
    def pubsub_subscription(
        topic_path: str,
        name: str,
        project: str = PROJECT,
    ) -> str:
        from google.cloud import pubsub

        subscriber = pubsub.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            project, Utils.hyphen_name(name)
        )
        subscription = subscriber.create_subscription(subscription_path, topic_path)

        logging.info(f"Created pubsub_subscription: {subscription.name}")
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
        logging.info(f"{cmd}")
        subprocess.run(cmd, check=True)
        logging.info(f"Deleted pubsub_subscription: {subscription.name}")

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
        logging.info(f"Starting publisher on {topic_path}")
        p = mp.Process(target=_infinite_publish_job)

        # We set the subprocess as a daemon so the main process doesn't wait for
        # the subprocess to finish. Since this is an infinite loop, it will
        # never finish, so it would cause the whole test to hang.
        # Typically, `terminate` should stop the subprocess during the fixture
        # cleanup phase, but we've had cases where the tests hang, most likely
        # due to concurrency issues with pytest running in parallel.
        #   https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.daemon
        p.daemon = True
        p.start()

        yield p.is_alive()

        # For cleanup, terminate the background process.
        logging.info("Stopping publisher")
        p.terminate()

    @staticmethod
    def cloud_build_submit(
        image_name: Optional[str] = None,
        config: Optional[str] = None,
        source: str = ".",
        substitutions: Optional[Dict[str, str]] = None,
        project: str = PROJECT,
    ) -> None:
        """Sends a Cloud Build job, if an image_name is provided it will be deleted at teardown."""
        cmd = ["gcloud", "auth", "configure-docker"]
        logging.info(f"{cmd}")
        subprocess.run(cmd, check=True)

        if substitutions:
            cmd_substitutions = [
                f"--substitutions={','.join([k + '=' + v for k, v in substitutions.items()])}"
            ]
        else:
            cmd_substitutions = []

        if config:
            try:
                with open(config) as f:
                    cmd = [
                        "gcloud",
                        "builds",
                        "submit",
                        f"--project={project}",
                        f"--config={config}",
                        *cmd_substitutions,
                        source,
                    ]
                    logging.info(f"{cmd}")
                    subprocess.run(cmd, check=True)
                    logging.info(f"Cloud build finished successfully: {config}")
                    yield f.read()
            except Exception as e:
                logging.exception(e)
                logging.warning(f"Current directory: {os.getcwd()}")
                yield config
        elif image_name:
            cmd = [
                "gcloud",
                "builds",
                "submit",
                f"--project={project}",
                f"--tag=gcr.io/{project}/{image_name}:{UUID}",
                *cmd_substitutions,
                source,
            ]
            logging.info(f"{cmd}")
            subprocess.run(cmd, check=True)
            logging.info(f"Created image: gcr.io/{project}/{image_name}:{UUID}")
            yield f"{image_name}:{UUID}"
        else:
            raise ValueError("must specify either `config` or `image_name`")

        if image_name:
            cmd = [
                "gcloud",
                "container",
                "images",
                "delete",
                f"gcr.io/{project}/{image_name}:{UUID}",
                f"--project={project}",
                "--force-delete-tags",
                "--quiet",
            ]
            logging.info(f"{cmd}")
            subprocess.run(cmd, check=True)
            logging.info(f"Deleted image: gcr.io/{project}/{image_name}:{UUID}")

    @staticmethod
    def dataflow_jobs_list(
        project: str = PROJECT, page_size: int = 30
    ) -> Iterable[dict]:
        from googleapiclient.discovery import build

        dataflow = build("dataflow", "v1b3")

        response = {"nextPageToken": None}
        while "nextPageToken" in response:
            # For more info see:
            #   https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/list
            request = (
                dataflow.projects()
                .jobs()
                .list(
                    projectId=project,
                    pageToken=response["nextPageToken"],
                    pageSize=page_size,
                )
            )
            response = request.execute()
            for job in response["jobs"]:
                yield job

    @staticmethod
    def dataflow_jobs_get(
        job_id: Optional[str] = None,
        job_name: Optional[str] = None,
        project: str = PROJECT,
        list_page_size: int = 30,
    ) -> Optional[Dict[str, Any]]:
        from googleapiclient.discovery import build

        dataflow = build("dataflow", "v1b3")

        if job_id:
            # For more info see:
            #   https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/get
            request = (
                dataflow.projects()
                .jobs()
                .get(
                    projectId=project,
                    jobId=job_id,
                    view="JOB_VIEW_SUMMARY",
                )
            )
            # If the job is not found, this throws an HttpError exception.
            job = request.execute()
            logging.info(f"Found Dataflow job: {job}")
            return job

        elif job_name:
            for job in Utils.dataflow_jobs_list(project, list_page_size):
                if job["name"] == job_name:
                    logging.info(f"Found Dataflow job: {job}")
                    return job
            raise ValueError(f"Dataflow job not found: job_name={job_name}")

        else:
            raise ValueError("must specify either `job_id` or `job_name`")

    @staticmethod
    def dataflow_jobs_wait(
        job_id: Optional[str] = None,
        job_name: Optional[str] = None,
        project: str = PROJECT,
        region: str = REGION,
        until_status: str = "JOB_STATE_DONE",
        list_page_size: int = 100,
        timeout_sec: str = TIMEOUT_SEC,
        poll_interval_sec: int = POLL_INTERVAL_SEC,
    ) -> Optional[str]:
        """For a list of all the valid states:
        https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs#Job.JobState
        """

        # Wait until we reach the desired status, or the job finished in some way.
        target_status = {
            until_status,
            "JOB_STATE_DONE",
            "JOB_STATE_FAILED",
            "JOB_STATE_CANCELLED",
            "JOB_STATE_DRAINED",
        }
        logging.info(
            f"Waiting for Dataflow job until {target_status}: job_id={job_id}, job_name={job_name}"
        )
        status = None
        for _ in range(0, timeout_sec, poll_interval_sec):
            try:
                job = Utils.dataflow_jobs_get(
                    job_id=job_id,
                    job_name=job_name,
                    project=project,
                    list_page_size=list_page_size,
                )
                status = job["currentState"]
                if status in target_status:
                    logging.info(
                        f"Job status {status} in {target_status}, done waiting"
                    )
                    return status
                elif status == "JOB_STATE_FAILED":
                    raise RuntimeError(
                        "Dataflow job failed:\n"
                        f"https://console.cloud.google.com/dataflow/jobs/{region}/{job_id}?project={project}"
                    )
                logging.info(
                    f"Job status {status} not in {target_status}, retrying in {poll_interval_sec} seconds"
                )
            except Exception as e:
                logging.exception(e)
            time.sleep(poll_interval_sec)
        if status is None:
            raise RuntimeError(
                f"Dataflow job not found: timeout_sec={timeout_sec}, target_status={target_status}, job_id={job_id}, job_name={job_name}"
            )
        else:
            raise RuntimeError(
                f"Dataflow job finished in status {status} but expected {target_status}: job_id={job_id}, job_name={job_name}"
            )

    @staticmethod
    def dataflow_jobs_cancel(
        job_id: str,
        drain: bool = False,
        project: str = PROJECT,
        region: str = REGION,
    ) -> None:
        logging.info(f"Cancelling Dataflow job ID: {job_id}")
        # We get an error using the googleapiclient.discovery APIs, probably
        # due to incompatible dependencies with apache-beam.
        # We use gcloud instead to cancel the job.

        if drain:
            # https://cloud.google.com/sdk/gcloud/reference/dataflow/jobs/drain
            cmd = [
                "gcloud",
                f"--project={project}",
                "dataflow",
                "jobs",
                "drain",
                job_id,
                f"--region={region}",
            ]
            logging.info(f"{cmd}")
            subprocess.run(cmd, check=True)

            # After draining the job, we must wait until the job has actually finished.
            Utils.dataflow_jobs_wait(job_id, project=project, region=region)

        else:
            # https://cloud.google.com/sdk/gcloud/reference/dataflow/jobs/cancel
            cmd = [
                "gcloud",
                f"--project={project}",
                "dataflow",
                "jobs",
                "cancel",
                job_id,
                f"--region={region}",
            ]
            logging.info(f"{cmd}")
            subprocess.run(cmd, check=True)

        logging.info(f"Cancelled Dataflow job: {job_id}")

    @staticmethod
    def dataflow_flex_template_build(
        bucket_name: str,
        image_name: str,
        metadata_file: str = "metadata.json",
        template_file: str = "template.json",
        project: str = PROJECT,
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
            f"--image=gcr.io/{project}/{image_name}",
            "--sdk-language=PYTHON",
            f"--metadata-file={metadata_file}",
        ]
        logging.info(f"{cmd}")
        subprocess.run(cmd, check=True)

        logging.info(f"dataflow_flex_template_build: {template_gcs_path}")
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
        unique_job_name = Utils.hyphen_name(job_name)
        logging.info(f"dataflow_job_name: {unique_job_name}")
        cmd = [
            "gcloud",
            "dataflow",
            "flex-template",
            "run",
            unique_job_name,
            f"--template-file-gcs-location={template_path}",
            f"--project={project}",
            f"--region={region}",
            f"--staging-location=gs://{bucket_name}/staging",
        ] + [
            f"--parameters={name}={value}"
            for name, value in {
                **parameters,
            }.items()
        ]
        logging.info(f"{cmd}")

        try:
            # The `capture_output` option was added in Python 3.7, so we must
            # pass the `stdout` and `stderr` options explicitly to support 3.6.
            # https://docs.python.org/3/library/subprocess.html#subprocess.run
            p = subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout = p.stdout.decode("utf-8")
            stderr = p.stderr.decode("utf-8")
            logging.info(f"Launched Dataflow Flex Template job: {unique_job_name}")
        except subprocess.CalledProcessError as e:
            logging.info(e, file=sys.stderr)
            stdout = e.stdout.decode("utf-8")
            stderr = e.stderr.decode("utf-8")
        finally:
            logging.info("--- stderr ---")
            logging.info(stderr)
            logging.info("--- stdout ---")
            logging.info(stdout)
            logging.info("--- end ---")
        return yaml.safe_load(stdout)["job"]["id"]


@pytest.fixture(scope="session")
def utils() -> Utils:
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"Test unique identifier: {UUID}")
    subprocess.run(["gcloud", "version"])
    return Utils()
