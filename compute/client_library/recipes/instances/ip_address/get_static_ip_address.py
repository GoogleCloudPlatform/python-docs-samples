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


# <REGION compute_ip_address_get_static_address>
# <IMPORTS/>

# <INGREDIENT get_static_ip_address />

# </REGION compute_ip_address_get_static_address>

if __name__ == "__main__":
    import google.auth

    PROJECT = google.auth.default()[1]
    region = "us-central1"
    address_name = "my-new-external-ip1"

    result = get_static_ip_address(PROJECT, address_name, region)
