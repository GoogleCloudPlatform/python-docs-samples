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
# limitations under the License.

"""
Sample Google App Engine application that demonstrates usage of the app
identity API to sign bytes and verify signatures.

For more information about App Engine, see README.md under /appengine.
"""

# [START all]

import base64

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util.asn1 import DerSequence
from google.appengine.api import app_identity
import webapp2


def verify_signature(data, signature, x509_certificate):
    """Verifies a signature using the given x.509 public key certificate."""

    # PyCrypto 2.6 doesn't support x.509 certificates directly, so we'll need
    # to extract the public key from it manually.
    # This code is based on https://github.com/google/oauth2client/blob/master
    # /oauth2client/_pycrypto_crypt.py
    pem_lines = x509_certificate.replace(b' ', b'').split()
    cert_der = base64.urlsafe_b64decode(b''.join(pem_lines[1:-1]))
    cert_seq = DerSequence()
    cert_seq.decode(cert_der)
    tbs_seq = DerSequence()
    tbs_seq.decode(cert_seq[0])
    public_key = RSA.importKey(tbs_seq[6])

    signer = PKCS1_v1_5.new(public_key)
    digest = SHA256.new(data)

    return signer.verify(digest, signature)


def verify_signed_by_app(data, signature):
    """Checks the signature and data against all currently valid certificates
    for the application."""
    public_certificates = app_identity.get_public_certificates()

    for cert in public_certificates:
        if verify_signature(data, signature, cert.x509_certificate_pem):
            return True

    return False


class MainPage(webapp2.RequestHandler):
    def get(self):
        message = 'Hello, world!'
        signing_key_name, signature = app_identity.sign_blob(message)
        verified = verify_signed_by_app(message, signature)

        self.response.content_type = 'text/plain'
        self.response.write('Message: {}\n'.format(message))
        self.response.write(
            'Signature: {}\n'.format(base64.b64encode(signature)))
        self.response.write('Verified: {}\n'.format(verified))


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

# [END all]
