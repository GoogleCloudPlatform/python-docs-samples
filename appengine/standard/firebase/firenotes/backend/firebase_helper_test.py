# Copyright 2016 Google Inc. All Rights Reserved.
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

import datetime
import os
import time

# Remove any existing pyjwt handlers, as firebase_helper will register
# its own.
try:
    import jwt
    jwt.unregister_algorithm('RS256')
except KeyError:
    pass

import mock
import pytest

import firebase_helper


def test_get_firebase_certificates(testbed):
    certs = firebase_helper.get_firebase_certificates()
    assert certs
    assert len(certs.keys())


@pytest.fixture
def test_certificate():
    from cryptography import utils
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.x509.oid import NameOID

    one_day = datetime.timedelta(1, 0, 0)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend())
    public_key = private_key.public_key()
    builder = x509.CertificateBuilder()

    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'example.com'),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'example.com'),
    ]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + one_day)
    builder = builder.serial_number(
        utils.int_from_bytes(os.urandom(20), "big") >> 1)
    builder = builder.public_key(public_key)

    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True)

    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend())

    certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)
    public_key_bytes = certificate.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo)
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())

    yield certificate, certificate_pem, public_key_bytes, private_key_bytes


def test_extract_public_key_from_certificate(test_certificate):
    _, certificate_pem, public_key_bytes, _ = test_certificate
    public_key = firebase_helper.extract_public_key_from_certificate(
        certificate_pem)
    assert public_key == public_key_bytes


def make_jwt(private_key_bytes, claims=None, headers=None):
    jwt_claims = {
        'iss': 'https://securetoken.google.com/test_audience',
        'aud': 'test_audience',
        'user_id': '123',
        'sub': '123',
        'iat': int(time.time()),
        'exp': int(time.time()) + 60,
        'email': 'user@example.com'
    }

    jwt_claims.update(claims if claims else {})
    if not headers:
        headers = {}

    return jwt.encode(
        jwt_claims, private_key_bytes, algorithm='RS256',
        headers=headers)


def test_verify_auth_token(test_certificate, monkeypatch):
    _, certificate_pem, _, private_key_bytes = test_certificate

    # The Firebase project ID is used as the JWT audience.
    monkeypatch.setenv('FIREBASE_PROJECT_ID', 'test_audience')

    # Generate a jwt to include in the request.
    jwt = make_jwt(private_key_bytes, headers={'kid': '1'})

    # Make a mock request
    request = mock.Mock()
    request.headers = {'Authorization': 'Bearer {}'.format(jwt)}

    get_cert_patch = mock.patch('firebase_helper.get_firebase_certificates')
    with get_cert_patch as get_cert_mock:
        # Make get_firebase_certificates return our test certificate.
        get_cert_mock.return_value = {'1': certificate_pem}
        claims = firebase_helper.verify_auth_token(request)

    assert claims['user_id'] == '123'


def test_verify_auth_token_no_auth_header():
    request = mock.Mock()
    request.headers = {}
    assert firebase_helper.verify_auth_token(request) is None


def test_verify_auth_token_invalid_key_id(test_certificate):
    _, _, _, private_key_bytes = test_certificate
    jwt = make_jwt(private_key_bytes, headers={'kid': 'invalid'})
    request = mock.Mock()
    request.headers = {'Authorization': 'Bearer {}'.format(jwt)}

    get_cert_patch = mock.patch('firebase_helper.get_firebase_certificates')
    with get_cert_patch as get_cert_mock:
        # Make get_firebase_certificates return no certificates
        get_cert_mock.return_value = {}
        assert firebase_helper.verify_auth_token(request) is None


def test_verify_auth_token_expired(test_certificate, monkeypatch):
    _, certificate_pem, _, private_key_bytes = test_certificate

    # The Firebase project ID is used as the JWT audience.
    monkeypatch.setenv('FIREBASE_PROJECT_ID', 'test_audience')

    # Generate a jwt to include in the request.
    jwt = make_jwt(
        private_key_bytes,
        claims={'exp': int(time.time()) - 60},
        headers={'kid': '1'})

    # Make a mock request
    request = mock.Mock()
    request.headers = {'Authorization': 'Bearer {}'.format(jwt)}

    get_cert_patch = mock.patch('firebase_helper.get_firebase_certificates')
    with get_cert_patch as get_cert_mock:
        # Make get_firebase_certificates return our test certificate.
        get_cert_mock.return_value = {'1': certificate_pem}
        assert firebase_helper.verify_auth_token(request) is None
