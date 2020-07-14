#!/usr/bin/env bash
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# run_tests_local.sh
#
# This script is a helper script for running tests with
# .kokoro/trampoline_v2.sh.
# run_tests_local.sh directory (sessions..)
#
# Example for running lint, py-3.6 and py-3.7 for cdn directory:
# $ cd cdn
# $ ../scripts/run_tests_local.sh .

set -euo pipefail

default_sessions=(
    "lint"
    "py-3.6"
    "py-3.7"
)

# The only required argument is a directory for running the tests.
if [[ $# -lt 1 ]]; then
    echo "Please provide at least one argument."
    echo "Usage: run_tests_local.sh directory (sessions..)"
    exit 1
fi

function repo_root() {
    local dir="$1"
    while [[ ! -d "${dir}/.git" ]]; do
	dir="$(dirname "$dir")"
    done
    echo "${dir}"
}

PROGRAM_PATH="$(realpath "$0")"
PROGRAM_DIR="$(dirname "${PROGRAM_PATH}")"
PROJECT_ROOT="$(repo_root "${PROGRAM_DIR}")"

directory="$(realpath "$1")"
relative_dir=${directory#"${PROJECT_ROOT}/"}
export RUN_TESTS_DIRS="${relative_dir}"

# We want to test this directory regardless of whether there's a change.
export TRAMPOLINE_BUILD_FILE=".kokoro/tests/run_tests_orig.sh"

if [[ $# -ge 2 ]]; then
    sessions=("${@:2}")
else
    sessions=("${default_sessions[@]}")
fi

echo "Running tests for directory: ${directory}"
echo "Sessions: ${sessions[@]}"

for session in "${sessions[@]}"
do
    export RUN_TESTS_SESSION="${session}"
    "${PROJECT_ROOT}/.kokoro/trampoline_v2.sh"
done
