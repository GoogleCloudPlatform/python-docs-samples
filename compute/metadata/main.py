#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Example of using the Compute Engine API to watch for maintenance notices.

For more information, see the README.md under /compute.
"""

# [START all]

import time

import requests


METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/"
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


def wait_for_maintenance(callback):
    url = METADATA_URL + 'instance/maintenance-event'
    last_in_maintenance = False
    # [START hanging_get]
    last_etag = 0

    while True:
        r = requests.get(
            url,
            params={'last_etag': last_etag},
            headers=METADATA_HEADERS)

        # During maintenance the service can return a 503, so these should
        # be retried.
        if r.status_code == 503:
            time.sleep(1)
            continue

        last_etag = r.headers['etag']
        # [END hanging_get]

        if r.text == 'MIGRATE_ON_HOST_MAINTENANCE':
            in_maintenance = True
        else:
            in_maintenance = False

        if in_maintenance != last_in_maintenance:
            last_in_maintenance = in_maintenance
            callback(in_maintenance)


def maintenance_callback(status):
    if status:
        print('Undergoing host maintenance')
    else:
        print('Finished host maintenance')


def main():
    wait_for_maintenance(maintenance_callback)


if __name__ == '__main__':
    main()
# [END all]
