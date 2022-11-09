#!/usr/bin/env python

# Copyright 2020 Google LLC
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

"""This application verifies HSM attestations using certificate bundles
obtained from Cloud HSM.

For more information, visit https://cloud.google.com/kms/docs/attest-key.
"""

# [START kms_verify_attestations]
import argparse
import gzip

from cryptography import exceptions
from cryptography import x509
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.asymmetric import padding
import pem


def verify(attestation_file, bundle_file):
    """Verifies an attestation using a bundle of certificates.

    Args:
      attestation_file: The name of the attestation file.
      bundle_file: The name of the bundle file containing the certificates
        used to verify the attestation.

    Returns:
      True if at least one of the certificates in bundle_file can verify the
      attestation data and its signature.
    """
    with gzip.open(attestation_file, 'rb') as f:
        # An attestation file consists of a data portion and a 256 byte
        # signature portion concatenated together.
        attestation = f.read()
        # Separate the components.
        data = attestation[:-256]
        signature = attestation[-256:]

        # Verify the attestation with one of the certificates in the bundle
        for cert in pem.parse_file(bundle_file):
            cert_obj = x509.load_pem_x509_certificate(
                str(cert).encode('utf-8'), backends.default_backend())
            try:
                # Check if the data was signed by the private key associated
                # with the public key in the certificate. The data should have
                # been signed with PKCS1v15 padding.
                cert_obj.public_key().verify(
                    signature, data, padding.PKCS1v15(),
                    cert_obj.signature_hash_algorithm)
                return True
            except exceptions.InvalidSignature:
                # Certificate bundles contain certificates that will not be
                # able to verify the attestation, so the InvalidSignature
                # errors can be ignored.
                continue
        return False
# [END kms_verify_attestations]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=__doc__)
    parser.add_argument('attestation_file', help="Name of attestation file.")
    parser.add_argument('bundle_file', help="Name of certificate bundle file.")

    args = parser.parse_args()

    if verify(args.attestation_file, args.bundle_file):
        print('Signature verified.')
    else:
        print('Signature verification failed.')
