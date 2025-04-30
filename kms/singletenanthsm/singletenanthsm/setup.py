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

import argparse
import ykman_utils
import gcloud_commands

def validate_operation(operation: str):
  if  operation == "build_custom_gcloud":
    try:
      gcloud_commands.build_custom_gcloud()
    except Exception as e:
      raise Exception(f"Generating custom gcloud build failed {e}")
  elif operation == "generate_rsa_keys":
    try: 
      ykman_utils.generate_private_key()
    except Exception as e:
      raise Exception(f"Generating private keys failed {e}")
  elif operation == "generate_gcloud_and_keys":
      generate_private_keys_build_gcloud()
  else:
    raise Exception("Operation type not valid. Operation flag value must be build_custom_gcloud,"
    " generate_rsa_keys, or generate_gcloud_and_keys")
 



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

  parser = argparse.ArgumentParser()
  parser.add_argument('--operation',type=str,
                      choices=['build_custom_gcloud','generate_rsa_keys','generate_gcloud_and_keys'],
                      required=True
                      )
  args = parser.parse_args()
  validate_operation(args.operation)
