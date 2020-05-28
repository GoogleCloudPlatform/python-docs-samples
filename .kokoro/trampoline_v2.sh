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

# trampoline_v2.sh
#
# This script does 3 things.
#
# 1. Prepare the Docker image for the test
# 2. Run the Docker with appropriate flags to run the test
# 3. Upload the newly built Docker image
#
# in a way that is somewhat compatible with trampoline_v1.
#
# To run this script, first download few files from gcs to /dev/shm.
# (/dev/shm is passed into the container as KOKORO_GFILE_DIR).
#
# gsutil cp gs://cloud-devrel-kokoro-resources/python-docs-samples/secrets_viewer_service_account.json /dev/shm
# gsutil cp gs://cloud-devrel-kokoro-resources/python-docs-samples/automl_secrets.txt /dev/shm
#
# Then run the script.
# .kokoro/trampoline_v2.sh
#
# These environment variables are required:
# TRAMPOLINE_IMAGE: The docker image to use.
# TRAMPOLINE_DOCKERFILE: The location of the Dockerfile.
#
# You can optionally change these environment variables:
# TRAMPOLINE_IMAGE_UPLOAD:
#     (true|false): Whether to upload the Docker image after the
#                   successful builds.
# TRAMPOLINE_BUILD_FILE: The script to run in the docker container.
# TRAMPOLINE_WORKSPACE: The workspace path in the docker container.
#                       Defaults to /workspace.
# TRAMPOLINE_SKIP_DOWNLOAD_IMAGE: Skip downloading the image when you
#                                 know you have the image locally.
#
# Potentially there are some repo specific envvars in .trampolinerc in
# the project root.


set -euo pipefail

if command -v tput >/dev/null && [[ -n "${TERM:-}" ]]; then
  readonly IO_COLOR_RED="$(tput setaf 1)"
  readonly IO_COLOR_GREEN="$(tput setaf 2)"
  readonly IO_COLOR_YELLOW="$(tput setaf 3)"
  readonly IO_COLOR_RESET="$(tput sgr0)"
else
  readonly IO_COLOR_RED=""
  readonly IO_COLOR_GREEN=""
  readonly IO_COLOR_YELLOW=""
  readonly IO_COLOR_RESET=""
fi

# Logs a message using the given color. The first argument must be one
# of the IO_COLOR_* variables defined above, such as
# "${IO_COLOR_YELLOW}". The remaining arguments will be logged in the
# given color. The log message will also have an RFC-3339 timestamp
# prepended (in UTC). You can disable the color output by setting
# TERM=vt100.
function log_impl() {
    local color="$1"
    shift
    local timestamp="$(date -u "+%Y-%m-%dT%H:%M:%SZ")"
    echo "================================================================"
    echo "${color}${timestamp}:" "$@" "${IO_COLOR_RESET}"
    echo "================================================================"
}

# Logs the given message with normal coloring and a timestamp.
function log() {
  log_impl "${IO_COLOR_RESET}" "$@"
}

# Logs the given message in green with a timestamp.
function log_green() {
  log_impl "${IO_COLOR_GREEN}" "$@"
}

# Logs the given message in yellow with a timestamp.
function log_yellow() {
  log_impl "${IO_COLOR_YELLOW}" "$@"
}

# Logs the given message in red with a timestamp.
function log_red() {
  log_impl "${IO_COLOR_RED}" "$@"
}

readonly tmpdir=$(mktemp -d -t ci-XXXXXXXX)
readonly tmphome="${tmpdir}/h"
mkdir -p "${tmphome}"

function cleanup() {
    rm -rf "${tmpdir}"
}
trap cleanup EXIT

function repo_root() {
    local dir="$1"
    while [[ ! -d "${dir}/.git" ]]; do
	dir="$(dirname "$dir")"
    done
    echo "${dir}"
}

# Temporarily limit the test to vision/automl
RUN_TESTS_DIRS="vision/automl"

PROGRAM_PATH="$(realpath "$0")"
PROGRAM_DIR="$(dirname "${PROGRAM_PATH}")"
PROJECT_ROOT="$(repo_root "${PROGRAM_DIR}")"

RUNNING_IN_CI="false"
TRAMPOLINE_V2="true"

# The workspace in the container, defaults to /workspace.
TRAMPOLINE_WORKSPACE="${TRAMPOLINE_WORKSPACE:-/workspace}"

# If it's running on Kokoro, RUNNING_IN_CI will be true and
# TRAMPOLINE_CI is set to 'kokoro'. Both envvars will be passing down
# to the container for telling which CI system we're in.
if [[ -n "${KOKORO_BUILD_ID:-}" ]]; then
    # descriptive env var for indicating it's on CI.
    RUNNING_IN_CI="true"
    TRAMPOLINE_CI="kokoro"
fi

# Configure the service account for pulling the docker image.
if [[ "${TRAMPOLINE_CI:-}" == "kokoro" ]]; then
    # Now we're re-using the trampoline service account.
    # Potentially we can pass down this key into Docker for
    # bootstrapping secret.
    SERVICE_ACCOUNT_KEY_FILE="${KOKORO_GFILE_DIR}/kokoro-trampoline.service-account.json"

    mkdir -p "${tmpdir}/gcloud"
    gcloud_config_dir="${tmpdir}/gcloud"

    log_yellow "Using isolated gcloud config: ${gcloud_config_dir}."
    export CLOUDSDK_CONFIG="${gcloud_config_dir}"

    log_yellow "Using ${SERVICE_ACCOUNT_KEY_FILE} for authentication."
    gcloud auth activate-service-account \
	   --key-file "${SERVICE_ACCOUNT_KEY_FILE}"
    gcloud auth configure-docker --quiet
fi

log_yellow "Changing to the project root: ${PROJECT_ROOT}."
cd "${PROJECT_ROOT}"

required_envvars=(
    # The basic trampoline configurations.
    "TRAMPOLINE_IMAGE"
    "TRAMPOLINE_BUILD_FILE"
)

pass_down_envvars=(
    # TRAMPOLINE_V2 variables.
    # Tells scripts whether they are running as part of CI or not.
    "RUNNING_IN_CI"
    # Indicates which CI system we're in.
    "TRAMPOLINE_CI"
    # Indicates we're running trampoline_v2.
    "TRAMPOLINE_V2"
    # KOKORO dynamic variables.
    "KOKORO_BUILD_NUMBER"
    "KOKORO_BUILD_ID"
    "KOKORO_JOB_NAME"
    "KOKORO_GIT_COMMIT"
    "KOKORO_GITHUB_COMMIT"
    "KOKORO_GITHUB_PULL_REQUEST_NUMBER"
    "KOKORO_GITHUB_PULL_REQUEST_COMMIT"
    # For Build Cop Bot
    "KOKORO_GITHUB_COMMIT_URL"
    "KOKORO_GITHUB_PULL_REQUEST_URL"
)

if [[ -f "${PROJECT_ROOT}/.trampolinerc" ]]; then
    source "${PROJECT_ROOT}/.trampolinerc"
fi

log_yellow "Checking environment variables."
for e in "${required_envvars[@]}"
do
    if [[ -z "${!e:-}" ]]; then
	log "Missing ${e} env var. Aborting."
	exit 1
    fi
done

if [[ "${TRAMPOLINE_SKIP_DOWNLOAD_IMAGE:-false}" == "true" ]]; then
    log_yellow "Re-using the local Docker image."
    has_cache="true"
else
    log_yellow "Preparing Docker image."
    # Download the docker image specified by `TRAMPOLINE_IMAGE`

    set +e  # ignore error on docker operations
    # We may want to add --max-concurrent-downloads flag.

    log_yellow "Start pulling the Docker image: ${TRAMPOLINE_IMAGE}."
    if docker pull "${TRAMPOLINE_IMAGE}"; then
	log_green "Finished pulling the Docker image: ${TRAMPOLINE_IMAGE}."
	has_cache="true"
    else
	log_red "Failed pulling the Docker image: ${TRAMPOLINE_IMAGE}."
	has_cache="false"
    fi
fi


# The default user for a Docker container has uid 0 (root). To avoid
# creating root-owned files in the build directory we tell docker to
# use the current user ID.
user_uid="$(id -u)"
user_gid="$(id -g)"
user_name="$(id -un)"

# To allow docker in docker, we add the user to the docker group in
# the host os.
docker_gid=$(cut -d: -f3 < <(getent group docker))

update_cache="false"
if [[ "${TRAMPOLINE_DOCKERFILE:-none}" != "none" ]]; then
    # Build the Docker image from the source.
    context_dir=$(dirname "${TRAMPOLINE_DOCKERFILE}")
    docker_build_flags=(
	"-f" "${TRAMPOLINE_DOCKERFILE}"
	"-t" "${TRAMPOLINE_IMAGE}"
	"--build-arg" "UID=${user_uid}"
	"--build-arg" "USERNAME=${user_name}"
    )
    if [[ "${has_cache}" == "true" ]]; then
	docker_build_flags+=("--cache-from" "${TRAMPOLINE_IMAGE}")
    fi

    log_yellow "Start building the docker image."
    if [[ "${TRAMPOLINE_SHOW_COMMAND:-false}" == "true" ]]; then
	echo "docker build" "${docker_build_flags[@]}" "${context_dir}"
    fi
    if docker build "${docker_build_flags[@]}" "${context_dir}"; then
	log_green "Finished building the docker image."
	update_cache="true"
    else
	log_red "Failed to build the Docker image. Aborting."
	exit 1
    fi
else
    if [[ "${has_cache}" != "true" ]]; then
	log_red "failed to download the image ${TRAMPOLINE_IMAGE}, aborting."
	exit 1
    fi
fi

# We use an array for the flags so they are easier to document.
docker_flags=(
    # Remove the container after it exists.
    "--rm"

    # Use the host network.
    "--network=host"

    # Run in priviledged mode. We are not using docker for sandboxing or
    # isolation, just for packaging our dev tools.
    "--privileged"

    # Run the docker script with the user id. Because the docker image gets to
    # write in ${PWD} you typically want this to be your user id.
    # To allow docker in docker, we need to use docker gid on the host.
    "--user" "${user_uid}:${docker_gid}"

    # Pass down the USER.
    "--env" "USER=${user_name}"

    # Mount the project directory inside the Docker container.
    "--volume" "${PROJECT_ROOT}:${TRAMPOLINE_WORKSPACE}"
    "--workdir" "${TRAMPOLINE_WORKSPACE}"
    "--env" "PROJECT_ROOT=${TRAMPOLINE_WORKSPACE}"

    # Mount the temporary home directory.
    "--volume" "${tmphome}:/h"
    "--env" "HOME=/h"

    # Allow docker in docker.
    "--volume" "/var/run/docker.sock:/var/run/docker.sock"

    # Mount the /tmp so that docker in docker can mount the files
    # there correctly.
    "--volume" "/tmp:/tmp"
    # Pass down the KOKORO_GFILE_DIR and KOKORO_KEYSTORE_DIR
    # TODO(tmatsuo): This part is not portable.
    "--env" "TRAMPOLINE_SECRET_DIR=/secrets"
    "--volume" "${KOKORO_GFILE_DIR:-/dev/shm}:/secrets/gfile"
    "--env" "KOKORO_GFILE_DIR=/secrets/gfile"
    "--volume" "${KOKORO_KEYSTORE_DIR:-/dev/shm}:/secrets/keystore"
    "--env" "KOKORO_KEYSTORE_DIR=/secrets/keystore"
)

# Add an option for nicer output if the build gets a tty.
if [[ -t 0 ]]; then
    docker_flags+=("-it")
fi

# Passing down env vars
for e in "${pass_down_envvars[@]}"
do
    if [[ -n "${!e:-}" ]]; then
	docker_flags+=("--env" "${e}=${!e}")
    fi
done

# If arguments are given, all arguments will become the commands run
# in the container, otherwise run TRAMPOLINE_BUILD_FILE.
if [[ $# -ge 1 ]]; then
    log_yellow "Running the given commands '" "${@:1}" "' in the container."
    readonly commands=("${@:1}")
    if [[ "${TRAMPOLINE_SHOW_COMMAND:-false}" == "true" ]]; then
	echo docker run "${docker_flags[@]}" "${TRAMPOLINE_IMAGE}" "${commands[@]}"
    fi
    docker run "${docker_flags[@]}" "${TRAMPOLINE_IMAGE}" "${commands[@]}"
else
    log_yellow "Running the tests in a Docker container."
    docker_flags+=("--entrypoint=${TRAMPOLINE_BUILD_FILE}")
    if [[ "${TRAMPOLINE_SHOW_COMMAND:-false}" == "true" ]]; then
	echo docker run "${docker_flags[@]}" "${TRAMPOLINE_IMAGE}"
    fi
    docker run "${docker_flags[@]}" "${TRAMPOLINE_IMAGE}"
fi


test_retval=$?

if [[ ${test_retval} -eq 0 ]]; then
    log_green "Build finished with ${test_retval}"
else
    log_red "Build finished with ${test_retval}"
fi

# Only upload it when the test passes.
if [[ "${update_cache}" == "true" ]] && \
       [[ $test_retval == 0 ]] && \
       [[ "${TRAMPOLINE_IMAGE_UPLOAD:-false}" == "true" ]]; then
    log_yellow "Uploading the Docker image."
    if docker push "${TRAMPOLINE_IMAGE}"; then
	log_green "Finished uploading the Docker image."
    else
	log_red "Failed uploading the Docker image."
    fi
fi

exit "${test_retval}"
