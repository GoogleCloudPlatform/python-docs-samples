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

# [START batch_notifications]
from google.cloud import batch_v1


def create_with_notifications(project_id: str, region: str, job_name: str, topic_name: str) -> batch_v1.Job:
    """
    This method shows how to create a sample Batch Job that will run
    a simple command with configured notifications.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/get-started#locations
        job_name: the name of the job that will be created.
            It needs to be unique for each project and region pair.
        topic_name: name of the Pub/Sub topic, where notifications will be sent.

    Returns:
        A job object representing the job created.
    """
    client = batch_v1.BatchServiceClient()

    # Define what will be done as part of the job.
    task = batch_v1.TaskSpec()
    runnable = batch_v1.Runnable()
    runnable.script = batch_v1.Runnable.Script()
    runnable.script.text = "echo Hello world! This is task ${BATCH_TASK_INDEX}. This job has a total of ${BATCH_TASK_COUNT} tasks."
    task.runnables = [runnable]
    task.max_retry_count = 2
    task.max_run_duration = "3600s"

    # Tasks are grouped inside a job using TaskGroups.
    # Currently, it's possible to have only one task group.
    group = batch_v1.TaskGroup()
    group.task_count = 4
    group.task_spec = task

    # Policies are used to define on what kind of virtual machines the tasks will run on.
    # Read more about local disks here: https://cloud.google.com/compute/docs/disks/persistent-disks
    policy = batch_v1.AllocationPolicy.InstancePolicy()
    policy.machine_type = "e2-standard-4"

    instances = batch_v1.AllocationPolicy.InstancePolicyOrTemplate()
    instances.policy = policy

    allocation_policy = batch_v1.AllocationPolicy()
    allocation_policy.instances = [instances]

    notification1 = batch_v1.JobNotification()
    notification1.pubsub_topic = f"projects/{project_id}/topics/{topic_name}"
    message1 = batch_v1.JobNotification.Message()
    message1.type_ = batch_v1.JobNotification.Type.JOB_STATE_CHANGED
    notification1.message = message1

    notification2 = batch_v1.JobNotification()
    notification2.pubsub_topic = f"projects/{project_id}/topics/{topic_name}"
    message2 = batch_v1.JobNotification.Message()
    message2.type_ = batch_v1.JobNotification.Type.TASK_STATE_CHANGED
    message2.new_task_state = batch_v1.TaskStatus.State.FAILED
    notification2.message = message2

    job = batch_v1.Job()
    job.task_groups = [group]
    job.allocation_policy = allocation_policy
    job.labels = {"env": "testing", "type": "script"}
    job.notifications = [notification1, notification2]

    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"

    return client.create_job(create_request)


# [END batch_notifications]

if __name__ == "__main__":
    import google.auth

    PROJECT = google.auth.default()[1]
    REGION = "europe-west4"
    topic_name = "some-topic"

    job = create_with_notifications(PROJECT, REGION, "notifications-job-batch", topic_name)
    print(job)
