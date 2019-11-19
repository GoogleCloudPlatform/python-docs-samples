import json
import requests
import time

"""Example of using the Metadata Server to watch deprecated endpoint accesses.

For more information, see the README.md under /compute.
"""


METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


# [START compute_wait_for_legacy_usage]
def wait_for_legacy_usage(callback):
    url = '{}/instance/legacy-endpoint-access'.format(METADATA_URL)
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
