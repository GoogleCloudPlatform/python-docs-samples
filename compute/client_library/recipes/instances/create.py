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
# flake8: noqa

# <REGION compute_instances_create>
# <IMPORTS/>

# <INGREDIENT get_image_from_family />

# <INGREDIENT disk_from_image />

# <INGREDIENT wait_for_extended_operation />

# <INGREDIENT create_instance />
# </REGION compute_instances_create>

if __name__ == "__main__":
    import uuid
    import google.auth
    import google.auth.exceptions

    try:
        default_project_id = google.auth.default()[1]
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        instance_name = "quickstart-" + uuid.uuid4().hex[:10]
        instance_zone = "europe-central2-b"

        newest_debian = get_image_from_family(
            project="debian-cloud", family="debian-10"
        )
        disk_type = f"zones/{instance_zone}/diskTypes/pd-standard"
        disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link)]

        create_instance(default_project_id, instance_zone, instance_name, disks)
