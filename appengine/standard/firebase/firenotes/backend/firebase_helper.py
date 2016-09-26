# Copyright 2016 Google Inc.
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

import json
import logging
import os
import ssl

from Crypto.Util import asn1
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors
import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
import jwt.exceptions


# For App Engine, pyjwt needs to use PyCrypto instead of Cryptography.
jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))

# [START fetch_certificates]
# This URL contains a list of active certificates used to sign Firebase
# auth tokens.
FIREBASE_CERTIFICATES_URL = (
    'https://www.googleapis.com/robot/v1/metadata/x509/'
    'securetoken@system.gserviceaccount.com')


# [START get_firebase_certificates]
def get_firebase_certificates():
    """Fetches the current Firebase certificates.

    Note: in a production application, you should cache this for at least
    an hour.
    """
    try:
        result = urlfetch.Fetch(
            FIREBASE_CERTIFICATES_URL,
            validate_certificate=True)
        data = result.content
    except urlfetch_errors.Error:
        logging.error('Error while fetching Firebase certificates.')
        raise

    certificates = json.loads(data)

    return certificates
# [END get_firebase_certificates]
# [END fetch_certificates]


# [START extract_public_key_from_certificate]
def extract_public_key_from_certificate(x509_certificate):
    """Extracts the PEM public key from an x509 certificate."""
    der_certificate_string = ssl.PEM_cert_to_DER_cert(x509_certificate)

    # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
    der_certificate = asn1.DerSequence()
    der_certificate.decode(der_certificate_string)
    tbs_certification = asn1.DerSequence()  # To Be Signed certificate
    tbs_certification.decode(der_certificate[0])

    subject_public_key_info = tbs_certification[6]

    return subject_public_key_info
# [END extract_public_key_from_certificate]


# [START verify_auth_token]
def verify_auth_token(request):
    """Verifies the JWT auth token in the request.

    If no token is found or if the token is invalid, returns None.
    Otherwise, it returns a dictionary containing the JWT claims.
    """
    if 'Authorization' not in request.headers:
        return None

    # Auth header is in format 'Bearer {jwt}'.
    request_jwt = request.headers['Authorization'].split(' ').pop()

    # Determine which certificate was used to sign the JWT.
    header = jwt.get_unverified_header(request_jwt)
    kid = header['kid']

    certificates = get_firebase_certificates()

    try:
        certificate = certificates[kid]
    except KeyError:
        logging.warning('JWT signed with unkown kid {}'.format(header['kid']))
        return None

    # Get the public key from the certificate. This is used to verify the
    # JWT signature.
    public_key = extract_public_key_from_certificate(certificate)

    # [START decrypt_token]
    try:
        claims = jwt.decode(
            request_jwt,
            public_key,
            algorithms=['RS256'],
            audience=os.environ['FIREBASE_PROJECT_ID'],
            issuer='https://securetoken.google.com/{}'.format(
                os.environ['FIREBASE_PROJECT_ID']))
    except jwt.exceptions.InvalidTokenError as e:
        logging.warning('JWT verification failed: {}'.format(e))
        return None
    # [END decrypt_token]

    return claims
# [END verify_auth_token]
