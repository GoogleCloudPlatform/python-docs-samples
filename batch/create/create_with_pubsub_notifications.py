#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import google.auth

# [START batch_notifications]
from google.cloud import batch_v1


def create_with_pubsub_notification_job(
    project_id: str, region: str, job_name: str, topic_name: str
) -> batch_v1.Job:
    """
    This method shows how to create a sample Batch Job that will run
    a simple command inside a container on Cloud Compute instances.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/locations
        job_name: the name of the job that will be created.
            It needs to be unique for each project and region pair.
        topic_name: the name of the Pub/Sub topic to which the notification will be sent.
            The topic should be created in GCP Pub/Sub before running this method.
            The procedure for creating a topic is listed here: https://cloud.google.com/pubsub/docs/create-topic

    Returns:
        A job object representing the job created.
    """

    client = batch_v1.BatchServiceClient()

    # Define what will be done as part of the job.
    runnable = batch_v1.Runnable()
    runnable.container = batch_v1.Runnable.Container()
    runnable.container.image_uri = "gcr.io/google-containers/busybox"
    runnable.container.entrypoint = "/bin/sh"
    runnable.container.commands = [
        "-c",
        "echo Hello world! This is task ${BATCH_TASK_INDEX}. This job has a total of ${BATCH_TASK_COUNT} tasks.",
    ]

    # Jobs can be divided into tasks. In this case, we have only one task.
    task = batch_v1.TaskSpec()
    task.runnables = [runnable]

    # We can specify what resources are requested by each task.
    resources = batch_v1.ComputeResource()
    resources.cpu_milli = 2000  # in milliseconds per cpu-second. This means the task requires 2 whole CPUs.
    resources.memory_mib = 16  # in MiB
    task.compute_resource = resources

    task.max_retry_count = 2
    task.max_run_duration = "3600s"

    # Tasks are grouped inside a job using TaskGroups.
    # Currently, it's possible to have only one task group.
    group = batch_v1.TaskGroup()
    group.task_count = 4
    group.task_spec = task

    # Policies are used to define on what kind of virtual machines the tasks will run on.
    # In this case, we tell the system to use "e2-standard-4" machine type.
    # Read more about machine types here: https://cloud.google.com/compute/docs/machine-types
    policy = batch_v1.AllocationPolicy.InstancePolicy()
    policy.machine_type = "e2-standard-4"
    instances = batch_v1.AllocationPolicy.InstancePolicyOrTemplate()
    instances.policy = policy
    allocation_policy = batch_v1.AllocationPolicy()
    allocation_policy.instances = [instances]

    job = batch_v1.Job()
    job.task_groups = [group]
    job.allocation_policy = allocation_policy
    job.labels = {"env": "testing", "type": "container"}
    # We use Cloud Logging as it's an out of the box available option
    job.logs_policy = batch_v1.LogsPolicy()
    job.logs_policy.destination = batch_v1.LogsPolicy.Destination.CLOUD_LOGGING

    # Configuring the first notification
    notification1 = batch_v1.JobNotification()
    notification1.pubsub_topic = f"projects/{project_id}/topics/{topic_name}"
    # Define the message that will be sent to the topic
    first_massage = batch_v1.JobNotification.Message()
    # Specify the new job state that will trigger the notification
    # In this case, the notification is triggered when the job state changes to SUCCEEDED
    first_massage.type_ = batch_v1.JobNotification.Type.JOB_STATE_CHANGED
    first_massage.new_job_state = batch_v1.JobStatus.State.SUCCEEDED
    # Assign the message to the notification
    notification1.message = first_massage

    # Configuring the second notification
    notification2 = batch_v1.JobNotification()
    notification2.pubsub_topic = f"projects/{project_id}/topics/{topic_name}"
    second_message = batch_v1.JobNotification.Message()
    second_message.type_ = batch_v1.JobNotification.Type.TASK_STATE_CHANGED
    second_message.new_task_state = batch_v1.TaskStatus.State.FAILED
    notification2.message = second_message

    # Assign a list of notifications to the job.
    job.notifications = [notification1, notification2]

    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"
    return client.create_job(create_request)


# [END batch_notifications]

if __name__ == "__main__":
    PROJECT_ID = google.auth.default()[1]
    REGION = "europe-west4"
    job_name = "your-job-name"
    # The topic should be created in GCP Pub/Sub
    existing_topic_name = "your-existing-topic-name"
    job = create_with_pubsub_notification_job(
        PROJECT_ID, REGION, job_name, existing_topic_name
    )
    print(job)
