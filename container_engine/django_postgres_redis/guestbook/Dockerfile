# Copyright 2015 Google Inc.
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
# limitations under the License

# The Google App Engine python runtime is Debian Jessie with Python installed
# and various os-level packages to allow installation of popular Python
# libraries. The source is on github at:
#   https://github.com/GoogleCloudPlatform/python-docker
FROM gcr.io/google_appengine/python

# Create a virtualenv for the application dependencies.
# If you want to use Python 3, add the -p python3.4 flag.
RUN virtualenv /env

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate. This ensures the application is executed within
# the context of the virtualenv and will have access to its dependencies.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Install dependencies.
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Uncomment the following line to use NODB
# NODB will use SQLite and in-memory cache insstead of Postgres And Redis
# This is useful to test the rest of the Django setup without configuring the database/cache
# Comment it out and rebuild this image once you have Postgres and Redis services in your cluster
ENV NODB 1

# Add application code.
ADD . /app

CMD export DJANGO_PASSWORD=$(cat /etc/secrets/djangouserpw); gunicorn -b :$PORT mysite.wsgi
