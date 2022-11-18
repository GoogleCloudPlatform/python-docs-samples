#!/usr/bin/env bash
# Copyright 2016 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All rights reserved.

set -v

curl -sSO "https://dl.google.com/cloudagents/install-logging-agent.sh"
chmod +x install-logging-agent.sh
./install-logging-agent.sh
mkdir -p /etc/google-fluentd/config.d/
cat <<EOF > /etc/google-fluentd/config.d/forward.conf
<source>
  type forward
  port 24224
</source>
EOF
service google-fluentd restart

apt-get update
apt-get install -yq \
        git build-essential supervisor python python-dev python-pip libffi-dev \
            libssl-dev
pip install fluent-logger

