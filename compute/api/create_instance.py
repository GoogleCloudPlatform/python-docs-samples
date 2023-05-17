#!/usr/bin/env python

# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of using the Compute Engine API to create and delete instances.

Creates a new compute engine instance and uses it to apply a caption to
an image.

    https://cloud.google.com/compute/docs/tutorials/python-guide

For more information, see the README.md under /compute.
"""

import argparse
import os
import time

import googleapiclient.discovery


# [START list_instances]
def list_instances(
        compute: object, 
        project: str, 
        zone: str,
) -> list:
    """Lists all instances in the specified zone.

    Args:
      compute: an initialized compute service object.
      project: the Google Cloud project ID.
      zone: the name of the zone in which the instances should be listed.

    Returns:
      A list of instances.
    """
    result = compute.instances().list(project=project, zone=zone).execute()
    return result["items"] if "items" in result else None


# [END list_instances]


# [START create_instance]
def create_instance(
        compute: object, 
        project: str, 
        zone: str, 
        name: str, 
        bucket: str,
) -> str:
    """Creates an instance in the specified zone.

    Args:
      compute: an initialized compute service object.
      project: the Google Cloud project ID.
      zone: the name of the zone in which the instances should be created.
      name: the name of the instance.
      bucket: the name of the bucket in which the image should be written.

    Returns:
      The instance object.
    """
    # Get the latest Debian Jessie image.
    image_response = (
        compute.images()
        .getFromFamily(project="debian-cloud", family="debian-11")
        .execute()
    )
    source_disk_image = image_response["selfLink"]

    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open(
        os.path.join(os.path.dirname(__file__), "startup-script.sh")
    ).read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    config = {
        "name": name,
        "machineType": machine_type,
        # Specify the boot disk and the image to use as a source.
        "disks": [
            {
                "boot": True,
                "autoDelete": True,
                "initializeParams": {
                    "sourceImage": source_disk_image,
                },
            }
        ],
        # Specify a network interface with NAT to access the public
        # internet.
        "networkInterfaces": [
            {
                "network": "global/networks/default",
                "accessConfigs": [{"type": "ONE_TO_ONE_NAT", "name": "External NAT"}],
            }
        ],
        # Allow the instance to access cloud storage and logging.
        "serviceAccounts": [
            {
                "email": "default",
                "scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/logging.write",
                ],
            }
        ],
        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        "metadata": {
            "items": [
                {
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    "key": "startup-script",
                    "value": startup_script,
                },
                {"key": "url", "value": image_url},
                {"key": "text", "value": image_caption},
                {"key": "bucket", "value": bucket},
            ]
        },
    }

    return compute.instances().insert(project=project, zone=zone, body=config).execute()


# [END create_instance]


# [START delete_instance]
def delete_instance(
        compute: object, 
        project: str, 
        zone: str, 
        name: str,
) -> str:
    """Deletes an instance.

    Args:
      compute: An initialized compute service object.
      project: The Google Cloud project ID.
      zone: The name of the zone in which the instances should be deleted.
      name: The name of the instance.

    Returns:
      Execute to delete the instance object.
    """
    return (
        compute.instances().delete(project=project, zone=zone, instance=name).execute()
    )


# [END delete_instance]


# [START wait_for_operation]
def wait_for_operation(
        compute: object, 
        project: str, 
        zone: str,
        operation: str,
) -> dict:
    """Waits for the given operation to complete.

    Args:
      compute: an initialized compute service object.
      project: the Google Cloud project ID.
      zone: the name of the zone in which the operation should be executed.
      operation: the operation ID.

    Returns:
      The result of the operation.
    """
    print("Waiting for operation to finish...")
    while True:
        result = (
            compute.zoneOperations()
            .get(project=project, zone=zone, operation=operation)
            .execute()
        )

        if result["status"] == "DONE":
            print("done.")
            if "error" in result:
                raise Exception(result["error"])
            return result

        time.sleep(1)


# [END wait_for_operation]


# [START run]
def main(
        project: str, 
        bucket: str,
        zone: str, 
        instance_name: str, 
        wait=True,
) -> None:
    """Runs the demo.

    Args:
      project: the Google Cloud project ID.
      bucket: the name of the bucket in which the image should be written.
      instance_name: the name of the instance.
      wait: whether to wait for the operation to complete.

    Returns:
      None.
    """
    compute = googleapiclient.discovery.build("compute", "v1")

    print("Creating instance.")

    operation = create_instance(compute, project, zone, instance_name, bucket)
    wait_for_operation(compute, project, zone, operation["name"])

    instances = list_instances(compute, project, zone)

    print(f"Instances in project {project} and zone {zone}:")
    for instance in instances:
        print(f' - {instance["name"]}')

    print(
        f"""
Instance created.
It will take a minute or two for the instance to complete work.
Check this URL: http://storage.googleapis.com/{bucket}/output.png
Once the image is uploaded press enter to delete the instance.
"""
    )

    if wait:
        input()

    print("Deleting instance.")

    operation = delete_instance(compute, project, zone, instance_name)
    wait_for_operation(compute, project, zone, operation["name"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID.")
    parser.add_argument("bucket_name", help="Your Google Cloud Storage bucket name.")
    parser.add_argument(
        "--zone", default="us-central1-f", help="Compute Engine zone to deploy to."
    )
    parser.add_argument("--name", default="demo-instance", help="New instance name.")

    args = parser.parse_args()

    main(args.project_id, args.bucket_name, args.zone, args.name)
# [END run]
