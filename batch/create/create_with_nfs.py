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

# [START batch_create_nfs_job]
from google.cloud import batch_v1


def create_job_with_network_file_system(
    project_id: str,
    region: str,
    job_name: str,
    mount_path: str,
    nfs_ip_address: str,
    nfs_path: str,
) -> batch_v1.Job:
    """
    Creates a Batch job with status events that mounts a Network File System (NFS).
    Function mounts an NFS volume using the provided NFS server, IP address and path.

    Args:
        project_id (str): project ID or project number of the Cloud project you want to use.
        region (str): name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/locations
        job_name (str): the name of the job that will be created.
            It needs to be unique for each project and region pair.
        mount_path (str): The mount path that the job's tasks use to access the NFS.
        nfs_ip_address (str): The IP address of the NFS server (e.g., Filestore instance).
            Documentation on how to create a
            Filestore instance is available here: https://cloud.google.com/filestore/docs/create-instance-gcloud
        nfs_path (str): The path of the NFS directory that the job accesses.
            The path must start with a / followed by the root directory of the NFS.

    Returns:
        batch_v1.Job: The created Batch job object containing configuration details.
    """
    client = batch_v1.BatchServiceClient()

    # Create a runnable with a script that writes a message to a file
    runnable = batch_v1.Runnable()
    runnable.script = batch_v1.Runnable.Script()
    runnable.script.text = f"echo Hello world from task ${{BATCH_TASK_INDEX}}. >> {mount_path}/output_task_${{BATCH_TASK_INDEX}}.txt"

    # Define a volume that uses NFS
    volume = batch_v1.Volume()
    volume.nfs = batch_v1.NFS(server=nfs_ip_address, remote_path=nfs_path)
    volume.mount_path = mount_path

    # Create a task specification and assign the runnable and volume to it
    task = batch_v1.TaskSpec()
    task.runnables = [runnable]
    task.volumes = [volume]

    # Specify what resources are requested by each task.
    resources = batch_v1.ComputeResource()
    resources.cpu_milli = 2000  # in milliseconds per cpu-second. This means the task requires 2 whole CPUs.
    resources.memory_mib = 16  # in MiB
    task.compute_resource = resources

    task.max_retry_count = 2
    task.max_run_duration = "3600s"

    # Create a task group and assign the task specification to it
    group = batch_v1.TaskGroup()
    group.task_count = 1
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

    # Create the job and assign the task group and allocation policy to it
    job = batch_v1.Job()
    job.task_groups = [group]
    job.allocation_policy = allocation_policy
    job.labels = {"env": "testing", "type": "container"}
    # We use Cloud Logging as it's an out of the box available option
    job.logs_policy = batch_v1.LogsPolicy()
    job.logs_policy.destination = batch_v1.LogsPolicy.Destination.CLOUD_LOGGING

    # Create the job request and set the job and job ID
    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"

    return client.create_job(create_request)


# [END batch_create_nfs_job]


if __name__ == "__main__":
    PROJECT_ID = google.auth.default()[1]
    REGION = "us-central1"
    job_name = "your-job-name"
    # The local path on your VM where the NFS mounted.
    mount_path = "/mnt/disks"
    # IP address of the NFS server e.g. Filestore instance.
    nfc_ip_address = "IP_address_of_your_NFS_server"
    # The path of the NFS directory
    nfs_path = "/your_nfs_path"
    create_job_with_network_file_system(
        PROJECT_ID, REGION, job_name, mount_path, nfc_ip_address, nfs_path
    )
