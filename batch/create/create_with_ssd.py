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

# [START batch_create_local_ssd_job]
from google.cloud import batch_v1


def create_local_ssd_job(
    project_id: str, region: str, job_name: str, ssd_name: str
) -> batch_v1.Job:
    """
    This method shows how to create a sample Batch Job that will run
    a simple command on Cloud Compute instances with mounted local SSD.
    Note: local SSD does not guarantee Local SSD data persistence.
    More details here: https://cloud.google.com/compute/docs/disks/local-ssd#data_persistence

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/get-started#locations
        job_name: the name of the job that will be created.
            It needs to be unique for each project and region pair.
        ssd_name: name of the local ssd to be mounted for your Job.

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

    volume = batch_v1.Volume()
    volume.device_name = ssd_name
    volume.mount_path = f"/mnt/disks/{ssd_name}"
    task.volumes = [volume]

    # Tasks are grouped inside a job using TaskGroups.
    # Currently, it's possible to have only one task group.
    group = batch_v1.TaskGroup()
    group.task_count = 4
    group.task_spec = task

    disk = batch_v1.AllocationPolicy.Disk()
    disk.type_ = "local-ssd"
    # The size of all the local SSDs in GB. Each local SSD is 375 GB,
    # so this value must be a multiple of 375 GB.
    # For example, for 2 local SSDs, set this value to 750 GB.
    disk.size_gb = 375
    assert(disk.size_gb % 375 == 0)
    assert(disk.size_gb % 375 == 0)

    # Policies are used to define on what kind of virtual machines the tasks will run on.
    # The allowed number of local SSDs depends on the machine type for your job's VMs.
    # In this case, we tell the system to use "n1-standard-1" machine type, which require to attach local ssd manually.
    # Read more about local disks here: https://cloud.google.com/compute/docs/disks/local-ssd#lssd_disk_options
    policy = batch_v1.AllocationPolicy.InstancePolicy()
    policy.machine_type = "n1-standard-1"

    attached_disk = batch_v1.AllocationPolicy.AttachedDisk()
    attached_disk.new_disk = disk
    attached_disk.device_name = ssd_name
    policy.disks = [attached_disk]

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


# [END batch_create_local_ssd_job]

if __name__ == "__main__":
    import google.auth

    PROJECT = google.auth.default()[1]
    REGION = "europe-west4"
    job = create_local_ssd_job(PROJECT, REGION, "ssd-job-batch", "local-ssd-0")
    print(job)
