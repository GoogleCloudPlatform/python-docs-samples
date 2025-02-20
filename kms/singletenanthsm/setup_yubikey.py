# Copyright 2025 Google LLC
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

import ykman_utils
import gcloud_commands

def generate_private_keys_build_gcloud():
  """Generates an RSA key on slot 82 of every yubikey
  connected to the local machine and builds the custom gcloud cli.
  """
  try: 
    ykman_utils.generate_private_key()
  except Exception as e:
    raise Exception(f"Generating private keys failed {e}")
  try:
    gcloud_commands.build_custom_gcloud()
  except Exception as e:
    raise Exception(f"Generating custom gcloud build failed {e}")

if __name__ == "__main__":

  generate_private_keys_build_gcloud()
