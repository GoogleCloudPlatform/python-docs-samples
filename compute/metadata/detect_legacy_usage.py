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

import json
import time

import requests


"""Example of using the Metadata Server to watch deprecated endpoint accesses.

For more information, see the README.md under /compute.
"""


METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


# [START compute_wait_for_legacy_usage]
def wait_for_legacy_usage(callback):
    url = f'{METADATA_URL}/instance/legacy-endpoint-access'
    last_etag = '0'
    counts = None
    while True:
        r = requests.get(
            url,
            params={
                'last_etag': last_etag,
                'recursive': True,
                'wait_for_change': True
            },
            headers=METADATA_HEADERS)
        if r.status_code == 503:  # Metadata server unavailable
            print('Metadata server unavailable. Sleeping for 1 second.')
            time.sleep(1)
            continue
        if r.status_code == 404:  # Feature not yet supported
            print('Legacy endpoint access not supported. Sleeping for 1 hour.')
            time.sleep(3600)
            continue
        r.raise_for_status()

        last_etag = r.headers['etag']
        access_info = json.loads(r.text)
        if not counts:
            counts = access_info
        if access_info != counts:
            diff = {
                ver: access_info[ver] - counts[ver] for ver in counts
            }
            counts = access_info
            callback(diff)
            # [END compute_wait_for_legacy_usage]


def legacy_callback(diff):
    print(
        'Since last message, {} new requests to 0.1 endpoints and {} new '
        'requests to v1beta1 endpoints.'.format(diff['0.1'], diff['v1beta1']))


def main():
    wait_for_legacy_usage(legacy_callback)


if __name__ == '__main__':
    main()
