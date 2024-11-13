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

# [START batch_create_gpu_job_n1]
from google.cloud import batch_v1


def create_gpu_job(
    project_id: str, region: str, zone: str, job_name: str
) -> batch_v1.Job:
    """
    This method shows how to create a sample Batch Job that will run
    a simple command on Cloud Compute instances on GPU machines.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/get-started#locations
        zone: name of the zone you want to use to run the job. Important in regard to GPUs availability.
            GPUs availability can be found here: https://cloud.google.com/compute/docs/gpus/gpu-regions-zones
        job_name: the name of the job that will be created.
            It needs to be unique for each project and region pair.

    Returns:
        A job object representing the job created.
    """
    client = batch_v1.BatchServiceClient()

    # Define what will be done as part of the job.
    task = batch_v1.TaskSpec()
    runnable = batch_v1.Runnable()
    runnable.script = batch_v1.Runnable.Script()
    runnable.script.text = "echo Hello world! This is task ${BATCH_TASK_INDEX}. This job has a total of ${BATCH_TASK_COUNT} tasks."
    # You can also run a script from a file. Just remember, that needs to be a script that's
    # already on the VM that will be running the job. Using runnable.script.text and runnable.script.path is mutually
    # exclusive.
    # runnable.script.path = '/tmp/test.sh'
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
    # Read more about machine types here: https://cloud.google.com/compute/docs/machine-types
    policy = batch_v1.AllocationPolicy.InstancePolicy()
    policy.machine_type = "n1-standard-16"

    accelerator = batch_v1.AllocationPolicy.Accelerator()
    # Note: not every accelerator is compatible with instance type
    # Read more here: https://cloud.google.com/compute/docs/gpus#t4-gpus
    accelerator.type_ = "nvidia-tesla-t4"
    accelerator.count = 1

    policy.accelerators = [accelerator]
    instances = batch_v1.AllocationPolicy.InstancePolicyOrTemplate()
    instances.policy = policy
    instances.install_gpu_drivers = True
    allocation_policy = batch_v1.AllocationPolicy()
    allocation_policy.instances = [instances]

    location = batch_v1.AllocationPolicy.LocationPolicy()
    location.allowed_locations = ["zones/us-central1-b"]
    allocation_policy.location = location

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


# [END batch_create_gpu_job_n1]


if __name__ == "__main__":
    import google.auth

    PROJECT = google.auth.default()[1]
    REGION = "europe-central2"
    ZONE = "europe-central2-b"
    job = create_gpu_job(PROJECT, REGION, ZONE, "gpu-job-batch")
    print(job)
