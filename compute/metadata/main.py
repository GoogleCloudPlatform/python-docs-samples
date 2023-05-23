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


METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


def wait_for_maintenance(callback):
    url = METADATA_URL + 'instance/maintenance-event'
    last_maintenance_event = None
    # [START hanging_get]
    last_etag = '0'

    while True:
        r = requests.get(
            url,
            params={'last_etag': last_etag, 'wait_for_change': True},
            headers=METADATA_HEADERS)

        # During maintenance the service can return a 503, so these should
        # be retried.
        if r.status_code == 503:
            time.sleep(1)
            continue
        r.raise_for_status()

        last_etag = r.headers['etag']
        # [END hanging_get]

        if r.text == 'NONE':
            maintenance_event = None
        else:
            maintenance_event = r.text

        if maintenance_event != last_maintenance_event:
            last_maintenance_event = maintenance_event
            callback(maintenance_event)


def maintenance_callback(event):
    if event:
        print(f'Undergoing host maintenance: {event}')
    else:
        print('Finished host maintenance')


def main():
    wait_for_maintenance(maintenance_callback)


if __name__ == '__main__':
    main()
# [END all]
