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

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa
from google.cloud import compute_v1


# <INGREDIENT get_instance_serial_port_output>
def get_instance_serial_port_output(project_id: str, zone: str, instance_name: str) -> compute_v1.SerialPortOutput:
    """
    Returns the last 1 MB of serial port output from the specified instance.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the VM instance you want to query.
    Returns:
        Content of the serial port output of an instance inside a compute_v1.SerialPortOutput object.
        More about this type: https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.types.SerialPortOutput

    """
    instance_client = compute_v1.InstancesClient()
    return instance_client.get_serial_port_output(project=project_id, zone=zone, instance=instance_name)
# </INGREDIENT>
