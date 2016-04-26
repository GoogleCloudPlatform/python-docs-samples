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

"""Example of authenticating using access tokens directly on Compute Engine.

For more information, see the README.md under /compute.
"""

# [START all]

import argparse
import base64
import os

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import requests


GOOGLE_PUBLIC_CERT_URL = (
    'https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem')


def get_google_public_cert_key():
    r = requests.get(GOOGLE_PUBLIC_CERT_URL)
    r.raise_for_status()

    # Load the certificate.
    certificate = x509.load_pem_x509_certificate(
        r.text.encode('utf-8'), default_backend())

    # Get the certicate's public key.
    public_key = certificate.public_key()

    return public_key


def wrap_rsa_key(public_key, private_key_bytes):
    # Use the Google public key to encrypt the customer private key.
    # This means that only the Google private key is capable of decrypting
    # the customer private key.
    wrapped_key = public_key.encrypt(
        private_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None))
    encoded_wrapped_key = base64.b64encode(wrapped_key)
    return encoded_wrapped_key


def main(key_file):
    # Generate a new 256-bit private key if no key is specified.
    if not key_file:
        customer_key_bytes = os.urandom(32)
    else:
        with open(key_file, 'rb') as f:
            customer_key_bytes = f.read()

    google_public_key = get_google_public_cert_key()
    wrapped_rsa_key = wrap_rsa_key(google_public_key, customer_key_bytes)

    print('Base-64 encoded private key: {}'.format(
        base64.b64encode(customer_key_bytes).decode('utf-8')))
    print('Wrapped RSA key: {}'.format(wrapped_rsa_key.decode('utf-8')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--key_file', help='File containing your binary private key.')

    args = parser.parse_args()

    main(args.key_file)
# [END all]
