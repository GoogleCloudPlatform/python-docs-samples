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


def delete_private_cloud_by_name(cloud_name: str):
    client = vmwareengine_v1.VmwareEngineClient()
    request = vmwareengine_v1.DeletePrivateCloudRequest()
    request.force = True
    request.name = cloud_name
    client.delete_private_cloud(request).result()
