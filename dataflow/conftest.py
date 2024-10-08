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

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import datetime
import itertools
import json
import logging
import multiprocessing as mp
import os
import platform
import re
import subprocess
import time
from typing import Any
import uuid

from google.api_core import retry
import pytest

TIMEOUT_SEC = 30 * 60  # 30 minutes (in seconds)


@pytest.fixture(scope="session")
def project() -> str:
    # This is set by the testing infrastructure.
    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    run_cmd("gcloud", "config", "set", "project", project)

    # Since everything requires the project, let's confiugre and show some
    # debugging information here.
    run_cmd("gcloud", "version")
    run_cmd("gcloud", "config", "list")
    return project


@pytest.fixture(scope="session")
def location() -> str:
    # Override for local testing.
    return os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")


@pytest.fixture(scope="session")
def unique_id() -> str:
    id = uuid.uuid4().hex[0:6]
    print(f"unique_id: {id}")
    return id


@pytest.fixture(scope="session")
def unique_name(test_name: str, unique_id: str) -> str:
    return f"{test_name.replace('/', '-')}-{unique_id}"


@pytest.fixture(scope="session")
def bucket_name(test_name: str, location: str, unique_id: str) -> Iterator[str]:
    # Override for local testing.
    if "GOOGLE_CLOUD_BUCKET" in os.environ:
        bucket_name = os.environ["GOOGLE_CLOUD_BUCKET"]
        print(f"bucket_name: {bucket_name} (from GOOGLE_CLOUD_BUCKET)")
        yield bucket_name
        return

    from google.cloud import storage

    storage_client = storage.Client()
    bucket_name = f"{test_name.replace('/', '-')}-{unique_id}"
    bucket = storage_client.create_bucket(bucket_name, location=location)

    print(f"bucket_name: {bucket_name}")
    yield bucket_name

    # Try to remove all files before deleting the bucket.
    # Deleting a bucket with too many files results in an error.
    try:
        run_cmd("gsutil", "-m", "rm", "-rf", f"gs://{bucket_name}/*")
    except RuntimeError:
        # If no files were found and it fails, ignore the error.
        pass

    # Delete the bucket.
    bucket.delete(force=True)


@pytest.fixture(scope="session")
def pubsub_topic(
    test_name: str, project: str, unique_id: str
) -> Iterator[Callable[[str], str]]:
    from google.cloud import pubsub

    publisher = pubsub.PublisherClient()
    created_topics = []

    def create_topic(name: str) -> str:
        unique_name = f"{test_name.replace('/', '-')}-{name}-{unique_id}"
        topic_path = publisher.topic_path(project, unique_name)
        topic = publisher.create_topic(name=topic_path)

        print(f"pubsub_topic created: {topic.name}")
        created_topics.append(topic.name)
        return topic.name

    yield create_topic

    for topic_path in created_topics:
        publisher.delete_topic(topic=topic_path)
        print(f"pubsub_topic deleted: {topic_path}")


@pytest.fixture(scope="session")
def pubsub_subscription(
    test_name: str, project: str, unique_id: str
) -> Iterator[Callable[[str, str], str]]:
    from google.cloud import pubsub

    subscriber = pubsub.SubscriberClient()
    created_subscriptions = []

    def create_subscription(name: str, topic_path: str) -> str:
        unique_name = f"{test_name.replace('/', '-')}-{name}-{unique_id}"
        subscription_path = subscriber.subscription_path(project, unique_name)
        subscription = subscriber.create_subscription(
            name=subscription_path, topic=topic_path
        )

        print(f"pubsub_subscription created: {subscription.name}")
        created_subscriptions.append(subscription.name)
        return subscription.name

    yield create_subscription

    for subscription_path in created_subscriptions:
        subscriber.delete_subscription(subscription=subscription_path)
        print(f"pubsub_subscription deleted: {subscription_path}")


def pubsub_publish(topic_path: str, messages: list[str]) -> None:
    from google.cloud import pubsub

    publisher = pubsub.PublisherClient()
    futures = [publisher.publish(topic_path, msg.encode("utf-8")) for msg in messages]
    _ = [future.result() for future in futures]  # wait synchronously
    print(f"pubsub_publish {len(messages)} message(s) to {topic_path}:")
    for msg in messages:
        print(f"- {repr(msg)}")


@retry.Retry(retry.if_exception_type(ValueError), timeout=TIMEOUT_SEC)
def pubsub_wait_for_messages(subscription_path: str) -> list[str]:
    from google.cloud import pubsub

    subscriber = pubsub.SubscriberClient()
    with subscriber:
        response = subscriber.pull(subscription=subscription_path, max_messages=10)
        messages = [m.message.data.decode("utf-8") for m in response.received_messages]
        if not messages:
            raise ValueError("pubsub_wait_for_messages no messages received")

        print(f"pubsub_receive got {len(messages)} message(s)")
        for msg in messages:
            print(f"- {repr(msg)}")

        ack_ids = [m.ack_id for m in response.received_messages]
        subscriber.acknowledge(subscription=subscription_path, ack_ids=ack_ids)
        print(f"pubsub_receive ack messages")
    return messages


def dataflow_job_url(project: str, location: str, job_id: str) -> str:
    return f"https://console.cloud.google.com/dataflow/jobs/{location}/{job_id}?project={project}"


@retry.Retry(retry.if_exception_type(LookupError), timeout=TIMEOUT_SEC)
def dataflow_find_job_by_name(project: str, location: str, job_name: str) -> str:
    from google.cloud import dataflow_v1beta3 as dataflow

    # https://cloud.google.com/python/docs/reference/dataflow/latest/google.cloud.dataflow_v1beta3.services.jobs_v1_beta3.JobsV1Beta3Client#google_cloud_dataflow_v1beta3_services_jobs_v1_beta3_JobsV1Beta3Client_list_jobs
    dataflow_client = dataflow.JobsV1Beta3Client()
    request = dataflow.ListJobsRequest(
        project_id=project,
        location=location,
    )
    for job in dataflow_client.list_jobs(request):
        if job.name == job_name:
            return job.id
    raise LookupError(f"dataflow_find_job_by_name job name not found: {job_name}")


@retry.Retry(retry.if_exception_type(ValueError), timeout=TIMEOUT_SEC)
def dataflow_wait_until_running(project: str, location: str, job_id: str) -> str:
    from google.cloud import dataflow_v1beta3 as dataflow
    from google.cloud.dataflow_v1beta3.types import JobView, JobState

    # https://cloud.google.com/python/docs/reference/dataflow/latest/google.cloud.dataflow_v1beta3.services.jobs_v1_beta3.JobsV1Beta3Client#google_cloud_dataflow_v1beta3_services_jobs_v1_beta3_JobsV1Beta3Client_get_job
    dataflow_client = dataflow.JobsV1Beta3Client()
    request = dataflow.GetJobRequest(
        project_id=project,
        location=location,
        job_id=job_id,
        view=JobView.JOB_VIEW_SUMMARY,
    )
    response = dataflow_client.get_job(request)

    job_url = dataflow_job_url(project, location, job_id)
    state = response.current_state
    if state == JobState.JOB_STATE_FAILED:
        raise RuntimeError(f"Dataflow job failed unexpectedly\n{job_url}")
    if state != JobState.JOB_STATE_RUNNING:
        raise ValueError(f"Dataflow job is not running, state: {state.name}\n{job_url}")
    return state.name


def dataflow_num_workers(project: str, location: str, job_id: str) -> int:
    from google.cloud import dataflow_v1beta3 as dataflow
    from google.cloud.dataflow_v1beta3.types import JobMessageImportance

    # https://cloud.google.com/python/docs/reference/dataflow/latest/google.cloud.dataflow_v1beta3.services.messages_v1_beta3.MessagesV1Beta3Client#google_cloud_dataflow_v1beta3_services_messages_v1_beta3_MessagesV1Beta3Client_list_job_messages
    dataflow_client = dataflow.MessagesV1Beta3Client()
    request = dataflow.ListJobMessagesRequest(
        project_id=project,
        location=location,
        job_id=job_id,
        minimum_importance=JobMessageImportance.JOB_MESSAGE_BASIC,
    )

    response = dataflow_client.list_job_messages(request)._response
    num_workers = [event.current_num_workers for event in response.autoscaling_events]
    if num_workers:
        return num_workers[-1]
    return 0


def dataflow_cancel_job(project: str, location: str, job_id: str) -> None:
    from google.cloud import dataflow_v1beta3 as dataflow
    from google.cloud.dataflow_v1beta3.types import Job, JobState

    # https://cloud.google.com/python/docs/reference/dataflow/latest/google.cloud.dataflow_v1beta3.services.jobs_v1_beta3.JobsV1Beta3Client#google_cloud_dataflow_v1beta3_services_jobs_v1_beta3_JobsV1Beta3Client_update_job
    dataflow_client = dataflow.JobsV1Beta3Client()
    request = dataflow.UpdateJobRequest(
        project_id=project,
        location=location,
        job_id=job_id,
        job=Job(requested_state=JobState.JOB_STATE_CANCELLED),
    )
    response = dataflow_client.update_job(request=request)
    print(response)


@retry.Retry(retry.if_exception_type(AssertionError), timeout=TIMEOUT_SEC)
def wait_until(condition: Callable[[], bool], message: str) -> None:
    assert condition(), message


def run_cmd(*cmd: str) -> subprocess.CompletedProcess:
    try:
        print(f"run_cmd: {cmd}")
        start = datetime.now()
        p = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(p.stderr.decode("utf-8").strip())
        print(p.stdout.decode("utf-8").strip())
        elapsed = (datetime.now() - start).seconds
        minutes = int(elapsed / 60)
        seconds = elapsed - minutes * 60
        print(f"-- run_cmd `{cmd[0]}` finished in {minutes}m {seconds}s")
        return p
    except subprocess.CalledProcessError as e:
        # Include the error message from the failed command.
        print(e.stderr.decode("utf-8"))
        print(e.stdout.decode("utf-8"))
        raise RuntimeError(f"{e}\n\n{e.stderr.decode('utf-8')}") from e


# ---- FOR BACKWARDS COMPATIBILITY ONLY, prefer fixture-style ---- #

# Default options.
UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"

POLL_INTERVAL_SEC = 60  # 1 minute in seconds
LIST_PAGE_SIZE = 100
TIMEOUT_SEC = 30 * 60  # 30 minutes in seconds

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
        if bucket_name := os.environ.get("GOOGLE_CLOUD_BUCKET"):
            logging.warning(f"Using bucket from GOOGLE_CLOUD_BUCKET: {bucket_name}")
            yield bucket_name
            return  # don't delete

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
        from google.api_core.exceptions import NotFound
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
        table = bigquery.Table(f"{project}.{dataset_name}.{table_name}", **kwargs)
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
    def bigquery_query(query: str, region: str = REGION) -> Iterator[dict[str, Any]]:
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
        image_name: str | None = None,
        config: str | None = None,
        source: str = ".",
        substitutions: dict[str, str] | None = None,
        project: str = PROJECT,
    ) -> None:
        """Sends a Cloud Build job, if an image_name is provided it will be deleted at teardown."""
        cmd = ["gcloud", "auth", "configure-docker"]
        logging.info(f"{cmd}")
        subprocess.check_call(cmd)
        gcr_project = project.replace(':', '/')

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
                f"--tag=gcr.io/{gcr_project}/{image_name}:{UUID}",
                *cmd_substitutions,
                source,
            ]
            logging.info(f"{cmd}")
            subprocess.check_call(cmd)
            logging.info(
                f"Created image: gcr.io/{gcr_project}/{image_name}:{UUID}")
            yield f"{image_name}:{UUID}"
        else:
            raise ValueError("must specify either `config` or `image_name`")

        if image_name:
            cmd = [
                "gcloud",
                "container",
                "images",
                "delete",
                f"gcr.io/{gcr_project}/{image_name}:{UUID}",
                f"--project={project}",
                "--force-delete-tags",
                "--quiet",
            ]
            logging.info(f"{cmd}")
            subprocess.check_call(cmd)
            logging.info(
                f"Deleted image: gcr.io/{gcr_project}/{image_name}:{UUID}")

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
    ) -> Iterator[dict]:
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
    def dataflow_jobs_get(job_id: str, project: str = PROJECT) -> dict[str, Any]:
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
        target_states: set[str] = {"JOB_STATE_DONE"},
        timeout_sec: int = TIMEOUT_SEC,
        poll_interval_sec: int = POLL_INTERVAL_SEC,
    ) -> str | None:
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
        assert job_is_done(), (
            f"Dataflow job is not done after {timeout_sec} seconds\n"
            + Utils.dataflow_job_url(job_id, project, region)
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
        metadata_file: str | None = "metadata.json",
        template_file: str = "template.json",
        project: str = PROJECT,
    ) -> str:
        # https://cloud.google.com/sdk/gcloud/reference/dataflow/flex-template/build
        template_gcs_path = f"gs://{bucket_name}/{template_file}"
        gcr_project = project.replace(':', '/')
        cmd = [
            "gcloud",
            "dataflow",
            "flex-template",
            "build",
            template_gcs_path,
            f"--project={project}",
            f"--image=gcr.io/{gcr_project}/{image_name}",
            "--sdk-language=PYTHON"
        ]
        if metadata_file:
            cmd.append(f"--metadata-file={metadata_file}")

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
        parameters: dict[str, str] = {},
        project: str = PROJECT,
        region: str = REGION,
        additional_experiments: dict[str,str] = {},
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
        ] + [
            f"--additional-experiments={name}={value}"
            for name, value in {
                **additional_experiments,
            }.items()
        ]
        logging.info(f"{cmd}")

        stdout = subprocess.check_output(cmd).decode("utf-8")
        logging.info(f"Launched Dataflow Flex Template job: {unique_job_name}")
        job_id = yaml.safe_load(stdout)["job"]["id"]
        logging.info(f"Dataflow Flex Template job id: {job_id}")
        logging.info(f">> {Utils.dataflow_job_url(job_id, project, region)}")
        yield job_id

        Utils.dataflow_jobs_cancel(job_id, region=region)

    @staticmethod
    def dataflow_extensible_template_run(
        job_name: str,
        template_path: str,
        bucket_name: str,
        parameters: dict[str, str] = {},
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
