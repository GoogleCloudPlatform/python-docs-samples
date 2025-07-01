#!/bin/bash


set -e


# Environment external variables.
GH_OWNER=$GH_OWNER
GH_REPOSITORY=$GH_REPOSITORY
GH_TOKEN=$GH_TOKEN


# Prepare internal variables.
GH_REPOSITORY_URL=https://github.com/${GH_OWNER}/${GH_REPOSITORY}
RUNNER_PREFIX="cloud-run-worker"
RUNNER_SUFFIX=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 5 | head -n 1)
RUNNER_NAME="${RUNNER_PREFIX}-${RUNNER_SUFFIX}"


# Configure the current runner instance with URL, token and name.
mkdir /home/docker/actions-runner && cd /home/docker/actions-runner
echo ${GH_REPOSITORY_URL}
./config.sh --unattended --url ${GH_REPOSITORY_URL} --token ${GH_TOKEN} --name ${RUNNER_NAME}


# Function to cleanup and remove runner from Github.
cleanup() {
   echo "Removing runner..."
./config.sh remove --unattended --token ${GH_TOKEN}
}


# Trap signals.
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM


# Run the runner.
./run.sh & wait $!
