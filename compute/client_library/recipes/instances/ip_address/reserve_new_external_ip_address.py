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


# <REGION compute_ip_address_reserve_new_external>
# <IMPORTS/>
# <INGREDIENT reserve_new_external_ip_address />

# </REGION compute_ip_address_reserve_new_external>

if __name__ == "__main__":
    import google.auth

    PROJECT = google.auth.default()[1]
    region = "us-central1"
    address_name = "my-new-external-ip"

    # ip4 global
    reserve_new_external_ip_address(PROJECT, address_name + "ip4-global")
    # ip4 regional premium
    reserve_new_external_ip_address(
        PROJECT,
        address_name + "ip4-regional-premium",
        region=region,
        is_premium=True,
    )
    # ip4 regional
    reserve_new_external_ip_address(
        PROJECT, address_name + "ip4-regional", region=region
    )
    # ip6 global
    reserve_new_external_ip_address(PROJECT, address_name + "ip6-global", is_v6=True)
    # ip6 regional
    reserve_new_external_ip_address(
        PROJECT, address_name + "ip6-regional", is_v6=True, region=region
    )
