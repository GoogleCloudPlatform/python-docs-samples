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
from google.api_core.exceptions import NotFound
import itertools
import json
import logging
import multiprocessing as mp
import os
import platform
import re
import subprocess
import time
from typing import Any, Callable, Dict, Iterable, Optional, Set
import uuid

import pytest

# Default options.
UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"

TIMEOUT_SEC = 30 * 60  # 30 minutes in seconds
POLL_INTERVAL_SEC = 60  # 1 minute in seconds
LIST_PAGE_SIZE = 100

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
    def wait_until(
        is_done: Callable[[], bool],
        timeout_sec: int = TIMEOUT_SEC,
        poll_interval_sec: int = POLL_INTERVAL_SEC,
    ) -> bool:
        for _ in range(0, timeout_sec, poll_interval_sec):
            if is_done():
                return True
            time.sleep(poll_interval_sec)
        return False

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
    def bigquery_dataset(
        name: str,
        project: str = PROJECT,
        location: str = REGION,
    ) -> str:
        from google.cloud import bigquery

        bigquery_client = bigquery.Client()

        dataset_name = Utils.underscore_name(name)
        dataset = bigquery.Dataset(f"{project}.{dataset_name}")
        dataset.location = location
        result = bigquery_client.create_dataset(dataset)

        logging.info(f"Created bigquery_dataset: {result.full_dataset_id}")
        yield result.dataset_id

        try:
            bigquery_client.delete_dataset(
                f"{project}.{dataset_name}", delete_contents=True
            )
            logging.info(f"Deleted bigquery_dataset: {result.full_dataset_id}")
        except NotFound:
            logging.info(f"{result.full_dataset_id} already deleted.")

    @staticmethod
    def bigquery_table(
        dataset_name: str, table_name: str, project: str = PROJECT, **kwargs
    ) -> str:
        from google.cloud import bigquery
        bigquery_client = bigquery.Client()
        table = bigquery.Table(
            f"{project}.{dataset_name}.{table_name}", **kwargs
        )
        result = bigquery_client.create_table(table)
        logging.info(f"Created bigquery_table: {result.full_table_id}")
        yield result.table_id
        # This table will be deleted when the dataset is deleted.

    @staticmethod
    def bigquery_table_exists(
        dataset_name: str, table_name: str, project: str = PROJECT
    ) -> bool:
        from google.cloud import bigquery
        from google.cloud.exceptions import NotFound

        bigquery_client = bigquery.Client()
        try:
            bigquery_client.get_table(f"{project}.{dataset_name}.{table_name}")
            return True
        except NotFound:
            return False

    @staticmethod
    def bigquery_query(query: str, region: str = REGION) -> Iterable[Dict[str, Any]]:
        from google.cloud import bigquery

        bigquery_client = bigquery.Client()
        logging.info(f"Bigquery query: {query}")
        for row in bigquery_client.query(query, location=region):
            yield dict(row)

    @staticmethod
    def pubsub_topic(name: str, project: str = PROJECT) -> str:
        from google.cloud import pubsub

        publisher_client = pubsub.PublisherClient()
        topic_path = publisher_client.topic_path(project, Utils.hyphen_name(name))
        topic = publisher_client.create_topic(request={"name": topic_path})

        logging.info(f"Created pubsub_topic: {topic.name}")
        yield topic.name

        # Due to the pinned library dependencies in apache-beam, client
        # library throws an error upon deletion.
        # We use gcloud for a workaround. See also:
        # https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4492
        cmd = ["gcloud", "pubsub", "--project", project, "topics", "delete", topic.name]
        logging.info(f"{cmd}")
        subprocess.check_call(cmd)
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
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )

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
        subprocess.check_call(cmd)
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
        subprocess.check_call(cmd)

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
                    subprocess.check_call(cmd)
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
            subprocess.check_call(cmd)
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
            subprocess.check_call(cmd)
            logging.info(f"Deleted image: gcr.io/{project}/{image_name}:{UUID}")

    @staticmethod
    def dataflow_job_url(
        job_id: str,
        project: str = PROJECT,
        region: str = REGION,
    ) -> str:
        return f"https://console.cloud.google.com/dataflow/jobs/{region}/{job_id}?project={project}"

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
    def dataflow_job_id(
        job_name: str, project: str = PROJECT, list_page_size: int = LIST_PAGE_SIZE
    ) -> str:
        for job in Utils.dataflow_jobs_list(project, list_page_size):
            if job["name"] == job_name:
                logging.info(f"Found Dataflow job: {job}")
                return job["id"]
        raise ValueError(f"Dataflow job not found: job_name={job_name}")

    @staticmethod
    def dataflow_jobs_get(job_id: str, project: str = PROJECT) -> Dict[str, Any]:
        from googleapiclient.discovery import build

        dataflow = build("dataflow", "v1b3")

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
        return request.execute()

    @staticmethod
    def dataflow_jobs_wait(
        job_id: str,
        project: str = PROJECT,
        region: str = REGION,
        target_states: Set[str] = {"JOB_STATE_DONE"},
        timeout_sec: str = TIMEOUT_SEC,
        poll_interval_sec: int = POLL_INTERVAL_SEC,
    ) -> Optional[str]:
        """For a list of all the valid states:
        https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs#Job.JobState
        """

        finish_states = {
            "JOB_STATE_DONE",
            "JOB_STATE_FAILED",
            "JOB_STATE_CANCELLED",
            "JOB_STATE_DRAINED",
        }
        logging.info(
            f"Waiting for Dataflow job {job_id} until {target_states}\n"
            + Utils.dataflow_job_url(job_id, project, region)
        )

        def job_is_done() -> bool:
            try:
                job = Utils.dataflow_jobs_get(job_id, project)
                state = job["currentState"]
                if state in target_states:
                    logging.info(f"Dataflow job found with state {state}")
                    return True
                elif state in finish_states:
                    raise RuntimeError(
                        f"Dataflow job finished with state {state}, but we were expecting {target_states}\n"
                        + Utils.dataflow_job_url(job_id, project, region)
                    )
                return False
            except Exception as e:
                logging.exception(e)
            return False

        Utils.wait_until(job_is_done, timeout_sec, poll_interval_sec)

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
            subprocess.check_call(cmd)

            # After draining the job, we must wait until the job has actually finished.
            Utils.dataflow_jobs_wait(
                job_id,
                target_states={
                    "JOB_STATE_DONE",
                    "JOB_STATE_FAILED",
                    "JOB_STATE_CANCELLED",
                    "JOB_STATE_DRAINED",
                },
                project=project,
                region=region,
            )

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
            subprocess.check_call(cmd)

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
        subprocess.check_call(cmd)

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

        stdout = subprocess.check_output(cmd).decode("utf-8")
        logging.info(f"Launched Dataflow Flex Template job: {unique_job_name}")
        job_id = yaml.safe_load(stdout)["job"]["id"]
        logging.info(f"Dataflow Flex Template job id: {job_id}")
        logging.info(f">> {Utils.dataflow_job_url(job_id, project, region)}")
        yield job_id

        Utils.dataflow_jobs_cancel(job_id)

    @staticmethod
    def dataflow_extensible_template_run(
        job_name: str,
        template_path: str,
        bucket_name: str,
        parameters: Dict[str, str] = {},
        project: str = PROJECT,
        region: str = REGION,
    ) -> str:
        import yaml

        unique_job_name = Utils.hyphen_name(job_name)
        logging.info(f"dataflow_job_name: {unique_job_name}")
        cmd = [
            "gcloud",
            "dataflow",
            "jobs",
            "run",
            unique_job_name,
            f"--gcs-location={template_path}",
            f"--project={project}",
            f"--region={region}",
            f"--staging-location=gs://{bucket_name}/staging",
        ] + [
            f"--parameters={name}={value}"
            for name, value in {
                **parameters,
            }.items()
        ]
        logging.info(cmd)

        stdout = subprocess.check_output(cmd).decode("utf-8")
        logging.info(f"Launched Dataflow Template job: {unique_job_name}")
        job_id = yaml.safe_load(stdout)["id"]
        logging.info(f"Dataflow Template job id: {job_id}")
        logging.info(f">> {Utils.dataflow_job_url(job_id, project, region)}")
        yield job_id

        Utils.dataflow_jobs_cancel(job_id)


@pytest.fixture(scope="session")
def utils() -> Utils:
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"Test unique identifier: {UUID}")
    subprocess.check_call(["gcloud", "version"])
    return Utils()
