#!/bin/bash

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Creates a zip archive of all files needed to run the key publisher.
# To run, just execute the script: `./package.sh`

set -e

CWD=$(pwd)
SRC_DIRECTORY=$(dirname "$0")
ZIP_DIR="/tmp/gcp_livestream_key_publisher"
OUTPUT_FILE="${CWD}/gcp_livestream_key_publisher_GENERIC_CONFIDENTIAL.zip"

if [[ -e "${OUTPUT_FILE}" ]]; then
  echo "File ${OUTPUT_FILE} already exists"
  exit 1
fi

cd "${SRC_DIRECTORY}"
mkdir "${ZIP_DIR}"
cp main.py main_test.py README.md api-config.template.yml requirements.txt "${ZIP_DIR}/"

mkdir "${ZIP_DIR}/clients"
cp clients/*.py "${ZIP_DIR}/clients/"
rm ${ZIP_DIR}/clients/keyos*

#mkdir "${ZIP_DIR}/third_party"
#cp third_party/*.py "${ZIP_DIR}/third_party/"

cd "$(dirname "${ZIP_DIR}")"
zip -r "${OUTPUT_FILE}" "$(basename "${ZIP_DIR}")"
rm -rf "${ZIP_DIR}"

echo "Successfully exported as ${OUTPUT_FILE}"
