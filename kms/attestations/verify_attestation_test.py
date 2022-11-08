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

import tempfile

import verify_attestation

# Test certificate bundles can be generated with the following steps:
# 1. Generate test key pairs.
#    - openssl genrsa -out test1.key 2048
#    - openssl genrsa -out test2.key 2048
# 2. Generate test certificates using the key pairs.
#    - openssl req -x509 -key test1.key -days 3650 -out test1.pem
#    - openssl req -x509 -key test2.key -days 3650 -out test2.pem
# 3. Create a bundle using the test certificates.
#    - cat test1.pem test2.pem > bundle.pem
# For instructions on downloading certificate bundles from Cloud HSM, refer to:
# https://cloud.google.com/kms/docs/attest-key#downloading_the_certificates
TEST_CERT_BUNDLE = b"""-----BEGIN CERTIFICATE-----
MIIDZDCCAkwCFE2PSNf++wMw+Jv86m41lbsa9aUMMA0GCSqGSIb3DQEBCwUAMFkx
CzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRl
cm5ldCBXaWRnaXRzIFB0eSBMdGQxEjAQBgNVBAMMCVRlc3QgQ2FyZDAeFw0yMDAz
MzEyMTQ0MjNaFw0zMDAzMjkyMTQ0MjNaMIGDMQswCQYDVQQGEwJBVTETMBEGA1UE
CAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRk
MSMwIQYDVQQLDBpjbG91ZC1rbXMtcHJvZC11cy1jZW50cmFsMTEXMBUGA1UEAwwO
VGVzdCBQYXJ0aXRpb24wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDh
cOk8hil8G4vl66jb02eXu2rKO6PmNF1GziXtzawyhx/+PDmEuGu+g/8hpivY6vDr
buAMFs8OIBBBlfED/soVANflXktDRGqWJau+rIrw9EGcclcwzlIboIi6KLPcLih0
N0TTxqRLgy2EsEQ6UKS7su4bOIxD3Z6FSeTsoq+C2sgSWXmLitO0iRYYcgRjoyCU
kdzzO/JCwPKhhQx5NUrrHseALaIltG4D0aWLuBZKyV38yA1XEMdyCGk7RedEYC+v
OzaJrNToQBCIaCdn3F0uqJd49irLNPyQ5CY3NNL8rupJSq3iVxhEIZ8ANaU8UDvo
5iaQNKV1/KiQsXfUW6fbAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAIIGB0aXhd6k
xyWgYzJ0DHpYP2ALwHRWXde5PtEkdHDguPlUTzZ5iTfqOJlEeUXlDO9RV82jc4mE
hguCaMl3Q+2JGLJLCnSDgcaY5WAVBF9FSakdbHBj4Ik9L8NDlUQB6Me4d4gKWpg1
bUD4n2KtvCZGZzA3pfRBcYyAbwC+xEi1XrITyshb0pkjsWO4Urg36W/RpkCiYAw0
Xua0jJMG/wcF+xktd7kgcsBh5Es2VCzyQwisXoOIi3EY7lMJK2+ctjQFy1GxumBU
jBlXj0VjAm3QOVLTh3mfb1XofoIjOOYkMBjXMiQhFy/Lv68u5q7qlEYe92OKxkCO
0UaAcqt8+QM=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDRjCCAi4CFBVm+eV+oRkaYq2NyuTfwxWapjFOMA0GCSqGSIb3DQEBCwUAMGYx
CzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRl
cm5ldCBXaWRnaXRzIFB0eSBMdGQxHzAdBgNVBAMMFlRlc3QgTWFudWZhY3R1cmVy
IFJvb3QwHhcNMjAwMzMxMjE0MjU1WhcNMzAwMzI5MjE0MjU1WjBZMQswCQYDVQQG
EwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lk
Z2l0cyBQdHkgTHRkMRIwEAYDVQQDDAlUZXN0IENhcmQwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQC28Wu0dusN6AYkYon8RIuHlJWWwZWlTxXSMK4v/IOY
pG9F2/gUEDMQOgpyCCpTc5eLHRPa/Z2QgB0c2VSlQC8FZ1l9/YL7uBTJ0UpDoBf8
LUimIqotneXpL+7CW1kWFLZIgpm0iVuTPjV2b3frtvu0B+nYuyo4dtToebqoOKse
F3ymLsAjSqA9aoCD0XbspAkLJIvdQU28vXY4Y2y0OTGUnaQ7ZDwkNLxeAfeIdNJD
FRCcYsLRopsyptFMYLLDrI70gywAGYaGOxYG8747BIZELyT5Gnt0o7JwpuF8Mi53
T5NGiu5/wLwXnxRRhb3M5+lStdTfvbEfgK1mC0ac8ym5AgMBAAEwDQYJKoZIhvcN
AQELBQADggEBAILH0Q8WlgaGBosPBjnpAsp4eZOfq9skKZERYzFA2wBAy4B0q9/S
3oL1MIZEU6/ckiFyAm3r4/ZxMLX0UrisuRQUFQ3w+gqFccqlmGETsZGJpPtfIm+n
JQo44XXnTHndqoYPNfvfQkp0WtJQS8hSgTASP+1GYjqOn1fZaa28m39/mx9Mrw7K
xtXOtrdKqJhWCWJPprfC5sYNCYTA2HXVmBU2Y4AP4A4w+A1gCAdzvH8EEyDjnvxJ
GEa4uczhA3n+NmhLipg1aGbxJO5ZHXdyFF2rTXVVXSiX8EEasnwcTDjeXDKhdpu6
biaxW9fnsJIXirAE03FFkC/tWelkGFkmMfs=
-----END CERTIFICATE-----"""

# Test attestations can be generated with the following steps:
# 1. Create a file containing the test attestation statement.
#    - echo "content" > attestation.dat
# 2. Sign the file with one the key pairs used to create the test certificates.
#    - openssl dgst -sha256 -sign test1.key -out signature.dat attestation.dat
# 3. Concatenate the signature to the statement to create an attestation.
#    - cat signature.dat >> attestation.dat
# 4. Compress the test attestation.
#    - gzip attestation.dat
# For instructions on downloading attestations from Cloud HSM, refer to:
# https://cloud.google.com/kms/docs/attest-key#downloading_the_attestation_statement
TEST_ATTESTATION_GZ = (
    b'\x1f\x8b\x08\x08\xda\xde\x84^\x00\x03attestation\x00\x01\x06\x01\xf9\xfe'
    b'\x15\xa7~W\xdazHq03\x95\xd1F\xcf\x1d\n\xe0\xbbv\x11\xed\xae\x186\xc0\xcc'
    b'.\xcf)\xf1?\xf7!\xf3\xd6M\x85\xfe\xb9\x84\xb2\x08V2(\xa1\x87]\xab\x01='
    b'\xb5\x0f)~\x06\xee\xfa/\x94\xa6x\x96o\xb1\xcb$\x82\x90\xe03J\t\x03\xf0'
    b'\xa4\xa5\xa9\xf9\xb2\xce\xdd2\xfam\x94W\x07\x00~\xa5\xc2\xcdq\xa1\x81'
    b'\x18\x83\xe0\xd9\x11k]\xbd\xf8\x81@\x9c*\x80\x91R\xb0\xae\x9d\x88\xb8T'
    b'\xd1>\xf6;\xe4\x83q%_\x8aw\x894\xb5:\xeab\xd2\x9a\x81\xdd\xa6\xf9\x94'
    b'\xff8\xb1\xed\x7fs\x0e\xc0\xde\x89\x00]\x8fL\x82\x8a\x11\x8f\\\xe483\x9d'
    b'&\x0b%\xfd\x0et\x8f\xa8\x1a\xb5K\xb4\xc7\x96\xd1}\x06\xdd\x93i\x1f\xc1@'
    b'\x92\xef}(B\x0f\xd1\x03\xaaYo\x9b\xad\xa9zw#\xc8\x9a\xad\x94\xfc\x07q]x'
    b'\xeb\xa2CA\xf8\xac\x96\xd9\xe5y4\xae]\x81\xb0$\x93\tx\xdb\xcc\x08:%\x1d'
    b'\xe2q\xaa\xc8:\xc2<C\xb5\x9b\xd1\xb0<\x12\x8a\x99f\x11\x9a"Q\x1d]\xac'
    b'\x81\xe2\x05\x06\x01\x00\x00')


def test_verify():
    with tempfile.NamedTemporaryFile() as attestation_file:
        with tempfile.NamedTemporaryFile() as bundle_file:
            attestation_file.write(TEST_ATTESTATION_GZ)
            bundle_file.write(TEST_CERT_BUNDLE)

            attestation_file.seek(0)
            bundle_file.seek(0)

            assert verify_attestation.verify(
                attestation_file.name, bundle_file.name)
