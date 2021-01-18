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

##
# retry.sh
# Provides utility function commonly needed across Cloud Build pipelines to
# retry commands on failure.
#
# Usage:
# 1. Retry single command:
#
# ./retry.sh "CMD"
#
# 2. Retry with check:
#
# ./retry.sh "gcloud RESOURCE EXISTS?" "gcloud ACTION"
#
##

# Usage: try "cmd1" "cmd2"
# If first cmd executes successfully then execute second cmd
runIfSuccessful() {
  echo "running: $1"
  $($1 > /dev/null)
  if [ $? -eq 0 ]; then
    echo "running: $2"
    $($2 > /dev/null)
  fi
}

# Define max retries
max_attempts=3;
attempt_num=1;

arg1="$1"
arg2="$2"

if [ $# -eq 1 ]
then
  cmd="$arg1"
else
  cmd="runIfSuccessful \"$arg1\" \"$arg2\""
fi

until eval $cmd
do
    if ((attempt_num==max_attempts))
    then
        echo "Attempt $attempt_num / $max_attempts failed! No more retries left!"
        exit
    else
        echo "Attempt $attempt_num / $max_attempts failed!"
        sleep $((attempt_num++))
    fi
done
