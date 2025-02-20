#!/usr/bin/env python

# Copyright 2020 Google LLC
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

import subprocess

command_build_custom_gcloud = """
  pushd /tmp
  curl -o installer.sh https://sdk.cloud.google.com
  chmod +x installer.sh
  ./installer.sh --disable-prompts --install-dir ~/sthi
  rm installer.sh
  popd
  alias sthigcloud=~/sthi/google-cloud-sdk/bin/gcloud
  sthigcloud auth login
  """


command_add_components = """
  ~/sthi/google-cloud-sdk/bin/gcloud components repositories add https://storage.googleapis.com/sthi-test-bucket/components-2.json
  ~/sthi/google-cloud-sdk/bin/gcloud components update
  """

def build_custom_gcloud():
  """Builds a custom gcloud binary."""
  try:
    print("\nBuilding custom gcloud build")
    process = subprocess.run(
        command_build_custom_gcloud,
        check=True,
        shell=True,
    )
    print(f"Return Test: {process}")
    print(f"Return Code: {process.returncode}")
    print(f"Standard Output: {process.stdout}")
    print(f"Standard Error: {process.stderr}")
    print("gcloud build executed successfully.")
    print(process.stdout)
  except subprocess.CalledProcessError as e:
    raise subprocess.CalledProcessError(f"Error executing gcloud build: {e}")
  try:
    print("\nAdding gcloud components")
    process = subprocess.run(
        command_add_components,
        check=False,
        capture_output=False,
        text=True,
        shell=True,
    )
    print(f"Return Test: {process}")
    print(f"Return Code: {process.returncode}")
    print(f"Standard Output: {process.stdout}")
    print(f"Standard Error: {process.stderr}")
    print("gcloud components add executed successfully.")
    print(process.stdout)
    return process
  except subprocess.CalledProcessError as e:
    raise subprocess.CalledProcessError(f"Error executing gcloud components update: {e}")
    print(f"Error executing gcloud components update: {e}")


command_gcloud_list_proposal = (
    "~/sthi/google-cloud-sdk/bin/gcloud kms single-tenant-hsm list "
    "--location=projects/hawksbill-playground/locations/global"
)

command_gcloud_describe_proposal = """
  ~/sthi/google-cloud-sdk/bin/gcloud \
  kms single-tenant-hsm proposal describe """

def fetch_challenges(sthi_proposal_resource:str):
  """Fetches challenges from the server."""

  challenges = []

  try:
    print("\nfetching challenges")
    process = subprocess.run(
        command_gcloud_describe_proposal + sthi_proposal_resource,
        capture_output=True,
        check=False,
        text=True,
        shell=True,
        # stderr=subprocess.STDOUT
    )
    print(f"Return Test: {process}")
    print(f"Return Code: {process.returncode}")
    print(f"Standard Output: {process.stdout}")
    print(f"Standard Error: {process.stderr}")
    print("gcloud command executed successfully.")
    print(process.stdout)
    return process
  except subprocess.CalledProcessError as e:
    raise subprocess.CalledProcessError(f"Error executing gcloud command: {e}")

  return challenges

command_gcloud_approve_proposal = [
    "~/sthi/google-cloud-sdk/bin/gcloud",
    "kms",
    "single-tenant-hsm",
    "proposal",
    "approve",
    "projects/hawksbill_playground/locations/global/singleTenantHsmInstances/my_instance/proposals/proposal1",
]

def send_signed_challenges():
  print("Sending signed challenges")
  try:

    process = subprocess.run(
        " ".join(command_gcloud_approve_proposal),
        capture_output=True,
        # check=True,
        text=True,
        shell=True,
    )
    print("gcloud command executed successfully.")
    return process

  except subprocess.CalledProcessError as e:
    raise subprocess.CalledProcessError(f"Error executing gcloud command: {e}")