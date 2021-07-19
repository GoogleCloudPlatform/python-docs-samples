#!/bin/bash
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

# A script to fetch gpg keys with retry.

function retry {
    if [[ "${#}" -le 1 ]]; then
	echo "Usage: ${0} retry_count commands.."
	exit 1
    fi
    local retries=${1}
    local command="${@:2}"
    until [[ "${retries}" -le 0 ]]; do
	$command && return 0
	if [[ $? -ne 0 ]]; then
	    echo "command failed, retrying"
	    ((retries--))
	fi
    done
    return 1
}

# 2.7.17 (Benjamin Peterson)
retry 3 gpg --recv-keys 04C367C218ADD4FF

# 3.6.9, 3.7.5 (Ned Deily)
retry 3 gpg --recv-keys 2D347EA6AA65421D
retry 3 gpg --recv-keys FB9921286F5E1540

# 3.8.0, 3.9.0 (Łukasz Langa)
retry 3 gpg --recv-keys B26995E310250568

# 3.10.x and 3.11.x (Pablo Galindo Salgado)
retry 3 gpg --recv-keys 64E628F8D684696D
