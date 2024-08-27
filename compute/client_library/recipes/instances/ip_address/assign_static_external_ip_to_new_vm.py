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
# flake8: noqa

# <REGION compute_ip_address_assign_static_new_vm>
# <IMPORTS/>

# <INGREDIENT get_image_from_family />


# <INGREDIENT disk_from_image />

# <INGREDIENT wait_for_extended_operation />


# <INGREDIENT create_instance />


# <INGREDIENT assign_static_external_ip_to_new_vm />
# </REGION compute_ip_address_assign_static_new_vm>

if __name__ == "__main__":
    import google.auth
    import uuid

    PROJECT = google.auth.default()[1]
    ZONE = "us-central1-a"
    instance_name = "quickstart-" + uuid.uuid4().hex[:10]
    ip_address = "34.343.343.34"  # put your IP here

    assign_static_external_ip_to_new_vm(
        PROJECT, ZONE, instance_name, external_ipv4=ip_address, external_access=True
    )
