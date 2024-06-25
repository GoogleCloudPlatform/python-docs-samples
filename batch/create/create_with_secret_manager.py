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

# [START batch_create_using_secret_manager]
from typing import Dict

from google.cloud import batch_v1


def create_with_secret_manager(
    project_id: str, region: str, job_name: str, secrets: Dict[str, str]
) -> batch_v1.Job:
    """
    This method shows how to create a sample Batch Job that will run
    a simple command on Cloud Compute instances with passing secrets from secret manager.
    Note: Job's service account should have the permissions to access secrets.
        - Secret Manager Secret Accessor (roles/secretmanager.secretAccessor) IAM role.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/get-started#locations
        job_name: the name of the job that will be created.
            It needs to be unique for each project and region pair.
        secrets: secrets, which should be passed to the job.
            The format should look like:
                - {'secret-name': 'projects/{project_id}/secrets/{secret_name}/versions/{version}'}
            version can be set to 'latest'.

    Returns:
        A job object representing the job created.
    """
    client = batch_v1.BatchServiceClient()

    # Define what will be done as part of the job.
    task = batch_v1.TaskSpec()
    runnable = batch_v1.Runnable()
    runnable.script = batch_v1.Runnable.Script()
    runnable.script.text = "echo Hello world! from task ${BATCH_TASK_INDEX}." + f" ${next(iter(secrets.keys()))} is the value of the secret."
    task.runnables = [runnable]
    task.max_retry_count = 2
    task.max_run_duration = "3600s"

    envable = batch_v1.Environment()
    envable.secret_variables = secrets
    task.environment = envable

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

    job = batch_v1.Job()
    job.task_groups = [group]
    job.allocation_policy = allocation_policy
    job.labels = {"env": "testing", "type": "script"}
    # We use Cloud Logging as it's an out of the box available option
    job.logs_policy = batch_v1.LogsPolicy()
    job.logs_policy.destination = batch_v1.LogsPolicy.Destination.CLOUD_LOGGING

    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"

    return client.create_job(create_request)


# [END batch_create_using_secret_manager]

if __name__ == "__main__":
    import google.auth

    PROJECT = google.auth.default()[1]
    REGION = "europe-west4"
    # Existing service account name within the project specified above.
    name = "test-account-name"
    secret_name = "TEST_SECRET"
    secrets = {secret_name: f"projects/11111111/secrets/{secret_name}/versions/latest"}
    job = create_with_secret_manager(PROJECT, REGION, "secret-manager-job-batch", secrets)
