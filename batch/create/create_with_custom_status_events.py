#  Copyright 2022 Google LLC
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

# [START batch_custom_events]
from google.cloud import batch_v1


def create_job_with_status_events(
    project_id: str, region: str, job_name: str
) -> batch_v1.Job:
    """
    This method shows the creation of a Batch job with custom status events which describe runnables
    Within the method, the state of a runnable is described by defining its display name.
    The script text is modified to change the commands that are executed, and barriers are adjusted
    to synchronize tasks at specific points.

    Args:
        project_id (str): project ID or project number of the Cloud project you want to use.
        region (str): name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/locations
        job_name (str): the name of the job that will be created.
            It needs to be unique for each project and region pair.

    Returns:
        A job object representing the job created with additional runnables and custom events.
    """
    client = batch_v1.BatchServiceClient()

    # Executes a simple script that prints a message.
    runn1 = batch_v1.Runnable()
    runn1.display_name = "Script 1"
    runn1.script.text = "echo Hello world from Script 1 for task ${BATCH_TASK_INDEX}"

    # Acts as a barrier to synchronize the execution of subsequent runnables.
    runn2 = batch_v1.Runnable()
    runn2.display_name = "Barrier 1"
    runn2.barrier = batch_v1.Runnable.Barrier({"name": "hello-barrier"})

    # Executes another script that prints a message, intended to run after the barrier.
    runn3 = batch_v1.Runnable()
    runn3.display_name = "Script 2"
    runn3.script.text = "echo Hello world from Script 2 for task ${BATCH_TASK_INDEX}"

    # Executes a script that imitates a delay and creates a custom event for monitoring purposes.
    runn4 = batch_v1.Runnable()
    runn4.script.text = (
        'sleep 30; echo \'{"batch/custom/event": "EVENT_DESCRIPTION"}\'; sleep 30'
    )

    # Jobs can be divided into tasks. In this case, we have only one task.
    task = batch_v1.TaskSpec()
    # Assigning a list of runnables to the task.
    task.runnables = [runn1, runn2, runn3, runn4]

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

    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"

    return client.create_job(create_request)


# [END batch_custom_events]


if __name__ == "__main__":
    PROJECT_ID = google.auth.default()[1]
    REGION = "europe-west4"
    job_name = "test-job-name"
    job = create_job_with_status_events(PROJECT_ID, REGION, job_name)
    print(job)
