# Copyright 2018 Google, Inc.
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

import argparse

"""This application demonstrates how to construct a Signed URL for objects in
   Google Cloud Storage.

For more information, see the README.md under /storage and the documentation
at https://cloud.google.com/storage/docs/access-control/signing-urls-manually.
"""

# [START storage_signed_url_all]
# [START storage_signed_url_dependencies]
import binascii
import collections
import datetime
import hashlib
import sys

# pip install six
from six.moves.urllib.parse import quote

# [START storage_signed_url_signer]
# pip install google-auth
from google.oauth2 import service_account

# [END storage_signed_url_signer]
# [END storage_signed_url_dependencies]


def generate_signed_url(service_account_file, bucket_name, object_name,
                        expiration, http_method='GET', query_parameters=None,
                        headers=None):

    if expiration > 604800:
        print('Expiration Time can\'t be longer than 604800 seconds (7 days).')
        sys.exit(1)

    # [START storage_signed_url_canonical_uri]
    escaped_object_name = quote(object_name, safe='')
    canonical_uri = '/{}/{}'.format(bucket_name, escaped_object_name)
    # [END storage_signed_url_canonical_uri]

    # [START storage_signed_url_canonical_datetime]
    datetime_now = datetime.datetime.utcnow()
    request_timestamp = datetime_now.strftime('%Y%m%dT%H%M%SZ')
    datestamp = datetime_now.strftime('%Y%m%d')
    # [END storage_signed_url_canonical_datetime]

    # [START storage_signed_url_credentials]
    # [START storage_signed_url_signer]
    google_credentials = service_account.Credentials.from_service_account_file(
        service_account_file)
    # [END storage_signed_url_signer]
    client_email = google_credentials.service_account_email
    credential_scope = '{}/auto/storage/goog4_request'.format(datestamp)
    credential = '{}/{}'.format(client_email, credential_scope)
    # [END storage_signed_url_credentials]

    if headers is None:
        headers = dict()
    # [START storage_signed_url_canonical_headers]
    headers['host'] = 'storage.googleapis.com'

    canonical_headers = ''
    ordered_headers = collections.OrderedDict(sorted(headers.items()))
    for k, v in ordered_headers.items():
        lower_k = str(k).lower()
        strip_v = str(v).lower()
        canonical_headers += '{}:{}\n'.format(lower_k, strip_v)
    # [END storage_signed_url_canonical_headers]

    # [START storage_signed_url_signed_headers]
    signed_headers = ''
    for k, _ in ordered_headers.items():
        lower_k = str(k).lower()
        signed_headers += '{};'.format(lower_k)
    signed_headers = signed_headers[:-1]  # remove trailing ';'
    # [END storage_signed_url_signed_headers]

    if query_parameters is None:
        query_parameters = dict()
    # [START storage_signed_url_canonical_query_parameters]
    query_parameters['X-Goog-Algorithm'] = 'GOOG4-RSA-SHA256'
    query_parameters['X-Goog-Credential'] = credential
    query_parameters['X-Goog-Date'] = request_timestamp
    query_parameters['X-Goog-Expires'] = expiration
    query_parameters['X-Goog-SignedHeaders'] = signed_headers

    canonical_query_string = ''
    ordered_query_parameters = collections.OrderedDict(
        sorted(query_parameters.items()))
    for k, v in ordered_query_parameters.items():
        encoded_k = quote(str(k), safe='')
        encoded_v = quote(str(v), safe='')
        canonical_query_string += '{}={}&'.format(encoded_k, encoded_v)
    canonical_query_string = canonical_query_string[:-1]  # remove trailing ';'
    # [END storage_signed_url_canonical_query_parameters]

    # [START storage_signed_url_canonical_request]
    canonical_request = '\n'.join([http_method,
                                   canonical_uri,
                                   canonical_query_string,
                                   canonical_headers,
                                   signed_headers,
                                   'UNSIGNED-PAYLOAD'])
    # [END storage_signed_url_canonical_request]

    # [START storage_signed_url_hash]
    canonical_request_hash = hashlib.sha256(
        canonical_request.encode()).hexdigest()
    # [END storage_signed_url_hash]

    # [START storage_signed_url_string_to_sign]
    string_to_sign = '\n'.join(['GOOG4-RSA-SHA256',
                                request_timestamp,
                                credential_scope,
                                canonical_request_hash])
    # [END storage_signed_url_string_to_sign]

    # [START storage_signed_url_signer]
    signature = binascii.hexlify(
        google_credentials.signer.sign(string_to_sign)
    ).decode()
    # [END storage_signed_url_signer]

    # [START storage_signed_url_construction]
    host_name = 'https://storage.googleapis.com'
    signed_url = '{}{}?{}&X-Goog-Signature={}'.format(host_name, canonical_uri,
                                                      canonical_query_string,
                                                      signature)
    # [END storage_signed_url_construction]
    return signed_url
# [END storage_signed_url_all]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('service_account_file',
                        help='Path to your Google service account.')
    parser.add_argument(
        'request_method', help='A request method, e.g GET, POST.')
    parser.add_argument('bucket_name', help='Your Cloud Storage bucket name.')
    parser.add_argument('object_name', help='Your Cloud Storage object name.')
    parser.add_argument('expiration', help='Expiration Time.')

    args = parser.parse_args()
    signed_url = generate_signed_url(
        service_account_file=args.service_account_file,
        http_method=args.request_method, bucket_name=args.bucket_name,
        object_name=args.object_name, expiration=int(args.expiration))

    print(signed_url)
