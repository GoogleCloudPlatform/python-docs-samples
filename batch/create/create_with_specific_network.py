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

# [START batch_create_custom_network]
from google.cloud import batch_v1


def create_with_custom_network(
    project_id: str,
    region: str,
    network_name: str,
    subnet_name: str,
    job_name: str,
) -> batch_v1.Job:
    """Create a Batch job that runs on a specific network and subnet.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/locations
        network_name: The name of a VPC network in the current project or a Shared VPC network.
        subnet_name: Name of the subnetwork to be used within the specified region.
        job_name: the name of the job that will be created.
            It needs to be unique for each project and region pair.
    Returns:
        A job object representing the job created.
    """

    client = batch_v1.BatchServiceClient()

    # Define what will be done as part of the job.
    runnable = batch_v1.Runnable()
    runnable.script = batch_v1.Runnable.Script()
    runnable.script.text = "echo Hello world! This is task ${BATCH_TASK_INDEX}. This job has a total of ${BATCH_TASK_COUNT} tasks."

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
    group.task_count = 3
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

    # Create a NetworkInterface object to specify network settings for the job
    network_interface = batch_v1.AllocationPolicy.NetworkInterface()
    # Set the network to the specified network name within the project
    network_interface.network = f"projects/{project_id}/global/networks/{network_name}"
    # Set the subnetwork to the specified subnetwork within the region
    network_interface.subnetwork = (
        f"projects/{project_id}/regions/{region}/subnetworks/{subnet_name}"
    )
    allocation_policy.network.network_interfaces = [network_interface]

    job = batch_v1.Job()
    job.task_groups = [group]
    job.allocation_policy = allocation_policy
    # We use Cloud Logging as it's an out of the box available option
    job.logs_policy = batch_v1.LogsPolicy()
    job.logs_policy.destination = batch_v1.LogsPolicy.Destination.CLOUD_LOGGING

    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"
    return client.create_job(create_request)


# [END batch_create_custom_network]

if __name__ == "__main__":
    PROJECT_ID = google.auth.default()[1]
    REGION = "europe-west"
    vpc_network = "VPC-network-name"
    subnet = "subnet-name"
    job_name = "test-job-name"
    job = create_with_custom_network(
        PROJECT_ID,
        REGION,
        vpc_network,
        subnet,
        job_name,
    )
