# Copyright 2023 Google LLC
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


from google.cloud import vmwareengine_v1
from google.longrunning.operations_pb2 import GetOperationRequest
from google.api_core.operation import Operation


def get_operation_by_name(operation_name: str) -> Operation:
    client = vmwareengine_v1.VmwareEngineClient()
    request = GetOperationRequest()
    request.name = operation_name
    return client.get_operation(request)


def get_operation(project_id: str, region: str, operation_id: str) -> Operation:
    return get_operation_by_name(f"projects/{project_id}/locations/{region}/operations/{operation_id}")
