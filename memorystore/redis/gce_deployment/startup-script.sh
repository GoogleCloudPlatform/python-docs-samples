#! /bin/bash

# Copyright 2018 Google Inc.
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
# [START memorystore_startup_script_sh]
set -v

# Talk to the metadata server to get the project id and location of application binary.
PROJECTID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/project/project-id" -H "Metadata-Flavor: Google")
GCS_APP_LOCATION=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/app-location" -H "Metadata-Flavor: Google")
REDISHOST=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/redis-host" -H "Metadata-Flavor: Google")
REDISPORT=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/redis-port" -H "Metadata-Flavor: Google")

# Install dependencies from apt
apt-get update
apt-get install -yq \
    git build-essential supervisor python python-dev python-pip libffi-dev \
    libssl-dev

# Install logging monitor. The monitor will automatically pickup logs send to
# syslog.
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &

gsutil cp $GCS_APP_LOCATION /app.tar
mkdir -p /app
tar -x -f /app.tar -C /app
cd /app

# Install the app dependencies
pip install --upgrade pip virtualenv
virtualenv /app/env
/app/env/bin/pip install -r /app/requirements.txt

# Create a pythonapp user. The application will run as this user.
getent passwd pythonapp || useradd -m -d /home/pythonapp pythonapp
chown -R pythonapp:pythonapp /app

# Configure supervisor to run the Go app.
cat >/etc/supervisor/conf.d/pythonapp.conf << EOF
[program:pythonapp]
directory=/app
environment=HOME="/home/pythonapp",USER="pythonapp",REDISHOST=$REDISHOST,REDISPORT=$REDISPORT
command=/app/env/bin/gunicorn main:app --bind 0.0.0:8080
autostart=true
autorestart=true
user=pythonapp
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update
# [END memorystore_startup_script_sh]
