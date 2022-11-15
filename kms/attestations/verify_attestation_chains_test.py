# Copyright 2021 Google LLC
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

from cryptography import x509
from cryptography.hazmat import backends
import pytest

import verify_attestation_chains

# The following keys and CSRs are needed to generate the test root certificates
# and certificate chains:
# 1. Test manufacturer root key pair.
#    - openssl genrsa -out mfr.key
# 2. Test owner root key pair.
#    - openssl genrsa -out owner.key
# 3. Test card key pair.
#    - openssl genrsa -out card.key
# 4. Test partition key pair.
#    - openssl genrsa -out partition.key
# 5. Test card CSR.
#    - openssl req -new -key card.key -out card.csr
# 6. Test partition CSR.
#    - openssl req -new -key partition.key -out partition.csr

# The manufacturer root certificate can be generated with the manufacturer root
# key:
# - openssl req -x509 -key mfr.key -days 3650 -out mfr.pem
TEST_MANUFACTURER_ROOT = b"""-----BEGIN CERTIFICATE-----
MIIDujCCAqKgAwIBAgIJAMs+bXbmbsuPMA0GCSqGSIb3DQEBCwUAMHIxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQxKzApBgNVBAMMIlRlc3QgTWFudWZhY3R1cmVyIFJvb3Qg
Q2VydGlmaWNhdGUwHhcNMjAwNDA4MTMzNDI1WhcNMzAwNDA2MTMzNDI1WjByMQsw
CQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJu
ZXQgV2lkZ2l0cyBQdHkgTHRkMSswKQYDVQQDDCJUZXN0IE1hbnVmYWN0dXJlciBS
b290IENlcnRpZmljYXRlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
242hKtNxBY2TLzyjIzFJtCf44WKha2A3KcfZ2Ul7Q/f6gAlLOK5/GvIsdB8MK/Y0
JgJBYUfPIZ8h0gLJVLhopopc4oOTRexCNCca97klSQCTZT4+wGqf/uIEF3PoL2Bb
uLhCQgxu+pPhfweBtEuqVcA33DYNN77J0f5KLKTHpOFEh1S1Q6ee/oRapj6J0hw6
a/7FW1R7329V5Nr9qRIzhnlpy2lBFfCV95yukAf9pUp1jCVkesugrkFY3U8np4Kn
KhO4x1jHTsTmfq/oCUzj/hiUtD8vlg//0ZL0SMFDCANM+shi/AbyWU1BCESLrKTa
kvI+atplTmLk8o6lOb+hMwIDAQABo1MwUTAdBgNVHQ4EFgQUlDYZuNfW4l4XDGiA
yvJjmAiTtR8wHwYDVR0jBBgwFoAUlDYZuNfW4l4XDGiAyvJjmAiTtR8wDwYDVR0T
AQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEADyDx4HpwOpDNnG+Mf4DiSFAk
ujYaWsQGB8hUXKuJLsLLtcPNTvwSa/umu/IhBVYop1GpTadAG5yjYULwPnM4GIt3
POffWAptw/a0XtFRxCXtvGlb+KvwQfYN8kq3weHcSvxTkrzgeWxs0LIQrZoaBPoo
MTJ88/s/p0d9Cf//5ukrW3LjF8OD8hd6HLpEie2qKc0wb6NXAuNgZ9m62kHSjXRS
Bd7Bwm5ZX3cOSz9SSseJKxEvD3lYUIF9w7gOeuifEpq2cfdT/VoiSL4GdN9wQ84R
0lM4loNrim85zL8YJdGAMlAQ5gbo9/Y8khSmoUOHHoV6P4UybOj+HEhDObhpQw==
-----END CERTIFICATE-----"""

TEST_MANUFACTURER_SUBJECT_BYTES = (
    b'0r1\x0b0\t\x06\x03U\x04\x06\x13\x02AU1\x130\x11\x06\x03U\x04\x08\x0c\n'
    b'Some-State1!0\x1f\x06\x03U\x04\n\x0c\x18Internet Widgits Pty Ltd1+0)\x06'
    b'\x03U\x04\x03\x0c"Test Manufacturer Root Certificate')

# The manufacturer certificate chain can be generated using the manufacturer
# root and card certificates, the manufacturer and card keys, and the card and
# partition CSRs:
# 1. Sign the card CSR with the manufacturer key and root certificate to create
#    the manufacturer card certificate:
#    - openssl x509 -req -in card.csr -CA mfr.pem -CAkey mfr.key -CAcreateserial  -out mfr_card.pem -days 365
# 2. Sign the partition CSR with the card key and manufacturer card certificate
#    to create the manufacturer partition certificate:
#    - openssl x509 -req -in partition.csr -CA mfr_card.pem -CAkey card.key -CAcreateserial  -out mfr_partition.pem -days 365
# 3. Create the manufacturer certificate chain using the manufacturer card and
#    partition certificates:
#    - cat mfr_partition.pem mfr_card.pem > mfr_chain.pem
TEST_MANUFACTURER_CHAIN = b"""-----BEGIN CERTIFICATE-----
MIIDSzCCAjMCCQDectxvPIHUkzANBgkqhkiG9w0BAQsFADBlMQswCQYDVQQGEwJB
VTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0
cyBQdHkgTHRkMR4wHAYDVQQDDBVUZXN0IENhcmQgQ2VydGlmaWNhdGUwHhcNMjAw
NDA4MTQ1NDAzWhcNMjEwNDA4MTQ1NDAzWjBqMQswCQYDVQQGEwJBVTETMBEGA1UE
CAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRk
MSMwIQYDVQQDDBpUZXN0IFBhcnRpdGlvbiBDZXJ0aWZpY2F0ZTCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAOKNNkMQXNHO9DnYcD+U8Ll/v9Z4v7oVJ2xV
YlDMMj2IJzhfZI77miii/ll3UZj3EDGC4y4pdS0L81988WWaQ4yVEZtgV5+WHLGr
Bb08Ex5qKRJ5ag2dI/Sz6+M9+5pI1wQ2TscqpFTIjYmBOB91CK96JJOKKtuPcDC1
31guMzTBpm3WiYyJBhR4Xj1McOwFLGBoPuZl9N8CzbqofVG1aTZi/C+AedU4YMjM
lKnB/Qxv94w6tsNPgbkjUGl3ZqmyUEKOG7zlIatnuXs70QEuv+KIouuFOTGiQppE
QaTNZ7UO0nhEG3e+cXyUzHxzlf8RTJpmhwqEHGnjF6YTsjVipGkCAwEAATANBgkq
hkiG9w0BAQsFAAOCAQEAD0rrWYZ+++ib6vvYi37j7hbwTuCRi1CSxXsrgiBFM1YK
cGzUnmqDXvJiBHX/qDIlkPxJy4AcfJ29r2dQ6kq1nwyaCAjqbGiFNR+VjNo4oAih
/xi1O1tIIZ4j979NAZmozsOXScYV1jVM/chM5QibDvdMp71YN8HwdMfGhssQe4sf
Kmu1IXq8XY/b0f/k3q5URgM+ur0qBJbqumY6fYgAYrfhSv7v4YlH2yqPVMWUOpHt
xFUKVbiXLux9xCsZ948b+lZLlETudUES5MpjHarlrr/CWxibjk6RJomN3eHHauZs
2ccag9KEQnjsBP2N2wqJeHU902attwvOoWQokUp9/Q==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDUzCCAjsCCQDNU9BSQM85jTANBgkqhkiG9w0BAQsFADByMQswCQYDVQQGEwJB
VTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0
cyBQdHkgTHRkMSswKQYDVQQDDCJUZXN0IE1hbnVmYWN0dXJlciBSb290IENlcnRp
ZmljYXRlMB4XDTIwMDQwODE0NTQwNloXDTIxMDQwODE0NTQwNlowZTELMAkGA1UE
BhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoMGEludGVybmV0IFdp
ZGdpdHMgUHR5IEx0ZDEeMBwGA1UEAwwVVGVzdCBDYXJkIENlcnRpZmljYXRlMIIB
IjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmVDLbIEpoVx9IzEalubKQuer
1iOI3c59gQDa9V6+iFBjmeOeE2vI97pojTAvWMWkRRKARklY3BruVKR5698yTLzb
cPwg3vqPvGNQFztJzaYAwRoerdT289upoEADdjQmA2Y7PF3zH88nLh74B9M5O8/t
jCfOWehl/ctUhTnIRCwEs7ZLMc3HHhG+puymhruD+hLNcgWfX2aizDEW8wpNZ6dd
JhGyA/OPXgFOhpqOZd/BFM/9w8rSBHfijitdNRK5UQj6TtRBykBj9ZvBzapRbLS/
rrqnSoXFo6dlZaxpJKXT/bFvx1ImZSizJln2klYcKv30g4lg+U4PaHvxNOFdrQID
AQABMA0GCSqGSIb3DQEBCwUAA4IBAQCtCrCZFLDYjEcKoMwbHa7XyELcQ79qM+YV
i2UBYZqvoq9ty0cLa1O1pvF35qbG1Z8B7dZ3rKwiXsBnFk87rMaweWvQWZkZEs3T
u4hBRdSrDCb2SEIEOusI49fZVhbZbgqnNX1AkFe9lqNVu82pYKpNSkP13cATVghB
mrDi6mxjdeiTHiek+ND05YEdGi38ja5T3/0PJjyEj35WXT+7CP95MArfNc3rhy6J
wkovm2tDYaojIJJtgFcBP3yhzsJOyHCkEzMqcOSjoT9pDv5qvrHKDMTZRKjcOgKP
YlIjHK237cZfoEh1PO2OI14sM2iD3ZpD5idGZI/GHF6GUWZ2AJqM
-----END CERTIFICATE-----"""

# The owner root certificate can be generated with the owner root key:
# - openssl req -x509 -key owner.key -days 3650 -out owner.pem
TEST_OWNER_ROOT = b"""-----BEGIN CERTIFICATE-----
MIIDrDCCApSgAwIBAgIJAJdbRMhyDhf+MA0GCSqGSIb3DQEBCwUAMGsxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQxJDAiBgNVBAMMG1Rlc3QgT3duZXIgUm9vdCBDZXJ0aWZp
Y2F0ZTAeFw0yMDA0MDgxMzM3MDVaFw0zMDA0MDYxMzM3MDVaMGsxCzAJBgNVBAYT
AkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRn
aXRzIFB0eSBMdGQxJDAiBgNVBAMMG1Rlc3QgT3duZXIgUm9vdCBDZXJ0aWZpY2F0
ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANwhPaA1nzlVrl1sFThl
GmwNSVczMmIVXOUyklTI2HIW7iHXWqqyusksQZJBvWpYLom0CzEv42wYWLtx5U9S
KE8P++DLCzspkV+KW11Gyyq5xsVxlrrcQZ6/SXDS8092IIZc/qht9Sgwv/u03tQA
JdwOgisnKRX2wtQfSi8lT+kNiT8IG6nbc1oRGcRa0cNY9uKaElF/EHxj33quZnQ0
tvxH7NhjxZ+GSiMbLChp3DZGnq9lcTurBFGPUe31riP5uThTiKA5DZDJadFSs8Q1
O0W0XPyWysm5y/7pAuz4yHZPdVzj6kssklHOE9+Yk3D8Q39n0utQJ84m+IrMrj8r
qSsCAwEAAaNTMFEwHQYDVR0OBBYEFCK8CyqtlBC06Hd9x680rN3nRJeZMB8GA1Ud
IwQYMBaAFCK8CyqtlBC06Hd9x680rN3nRJeZMA8GA1UdEwEB/wQFMAMBAf8wDQYJ
KoZIhvcNAQELBQADggEBAHXopvAk9qAqsW6tK9YmRy+EXCqxoOuKdXlU75G1GVnX
Obk/1DCbT2/ioXmSeA15p7fFdf5JG4J7ejCfJG8uXrKb0JW0RWRGXmGnO967FejD
STV8tp/uAYduPVcR9EqVDfOKU2jf0MoZnP95/dlBxZ+yTMnuusBu8z7ERPsQWve8
yitpRkFz9nrFytZRJVJxl+bm0Llz2eqINYR3Oia7v0xtS1XaJUGX5mG2gpMlIfpu
1ByJP8g11f9HW84eeZ9ceKU848uJtj+DTDnx4Ck1x6huMvZkxOAVTNWmT1+osDv7
vsVkjBnGwXfcAv6jFQiErcdpZ1MVdLxsAFHrAvYH67E=
-----END CERTIFICATE-----"""

# The owner card certificate chain can be generated using the owner
# root certificate, the owner key, and the card CSR.
# 1. Sign the card CSR with the owner root certificate to create the
#    owner card certificate:
#    - openssl x509 -req -in card.csr -CA owner.pem -CAkey owner.key -CAcreateserial  -out owner_card_chain.pem -days 365
TEST_OWNER_CARD_CHAIN = b"""-----BEGIN CERTIFICATE-----
MIIDTDCCAjQCCQDp+9ouYgrR0DANBgkqhkiG9w0BAQsFADBrMQswCQYDVQQGEwJB
VTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0
cyBQdHkgTHRkMSQwIgYDVQQDDBtUZXN0IE93bmVyIFJvb3QgQ2VydGlmaWNhdGUw
HhcNMjAwNDA4MTYyMTEyWhcNMjEwNDA4MTYyMTEyWjBlMQswCQYDVQQGEwJBVTET
MBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQ
dHkgTHRkMR4wHAYDVQQDDBVUZXN0IENhcmQgQ2VydGlmaWNhdGUwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQCZUMtsgSmhXH0jMRqW5spC56vWI4jdzn2B
ANr1Xr6IUGOZ454Ta8j3umiNMC9YxaRFEoBGSVjcGu5UpHnr3zJMvNtw/CDe+o+8
Y1AXO0nNpgDBGh6t1Pbz26mgQAN2NCYDZjs8XfMfzycuHvgH0zk7z+2MJ85Z6GX9
y1SFOchELASztksxzcceEb6m7KaGu4P6Es1yBZ9fZqLMMRbzCk1np10mEbID849e
AU6Gmo5l38EUz/3DytIEd+KOK101ErlRCPpO1EHKQGP1m8HNqlFstL+uuqdKhcWj
p2VlrGkkpdP9sW/HUiZlKLMmWfaSVhwq/fSDiWD5Tg9oe/E04V2tAgMBAAEwDQYJ
KoZIhvcNAQELBQADggEBAM3hz+TfQNaeuBgPyqBedN6QkhSiTdzpNG7Eyfw3Sx8n
OSuZxcsZgNRo+WNJt4zi9cMaOwgPcuoGCW7Iw2StEtBqgujlExrfUHzu17yoBHxQ
DTvi7QRHb6W2amsSKcuoFkI1txVmVWQA2HkSQVqIzZZoI3qVu2cQMyVHG7MKPHFU
5Mzw0H37gfttXYnUDZM84ETpGuf7EXA7ROdgwDvDD8CqOMDBKpKqau9QVh4aBZW4
koGMoga+RwjNt4FVCW4F4qn43fteDSmxdUuxqCn6V7CpRlHIc8J2q9nzsne/NCA0
2W+pXJD8hjvb9YQuXyV1QOaV6dcDLDcKG6NCdtxisxM=
-----END CERTIFICATE-----"""

# The owner partition certificate chain can be generated using the owner
# root certificate, the owner key, and the partition CSR.
# 1. Sign the partition CSR with the owner key and root certificate to create
#    the owner partition certificate:
#    - openssl x509 -req -in partition.csr -CA owner.pem -CAkey owner.key -CAcreateserial  -out owner_partition_chain.pem -days 365
TEST_OWNER_PARTITION_CHAIN = b"""-----BEGIN CERTIFICATE-----
MIIDUTCCAjkCCQDp+9ouYgrR0TANBgkqhkiG9w0BAQsFADBrMQswCQYDVQQGEwJB
VTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0
cyBQdHkgTHRkMSQwIgYDVQQDDBtUZXN0IE93bmVyIFJvb3QgQ2VydGlmaWNhdGUw
HhcNMjAwNDA4MTYyNDQ0WhcNMjEwNDA4MTYyNDQ0WjBqMQswCQYDVQQGEwJBVTET
MBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQ
dHkgTHRkMSMwIQYDVQQDDBpUZXN0IFBhcnRpdGlvbiBDZXJ0aWZpY2F0ZTCCASIw
DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOKNNkMQXNHO9DnYcD+U8Ll/v9Z4
v7oVJ2xVYlDMMj2IJzhfZI77miii/ll3UZj3EDGC4y4pdS0L81988WWaQ4yVEZtg
V5+WHLGrBb08Ex5qKRJ5ag2dI/Sz6+M9+5pI1wQ2TscqpFTIjYmBOB91CK96JJOK
KtuPcDC131guMzTBpm3WiYyJBhR4Xj1McOwFLGBoPuZl9N8CzbqofVG1aTZi/C+A
edU4YMjMlKnB/Qxv94w6tsNPgbkjUGl3ZqmyUEKOG7zlIatnuXs70QEuv+KIouuF
OTGiQppEQaTNZ7UO0nhEG3e+cXyUzHxzlf8RTJpmhwqEHGnjF6YTsjVipGkCAwEA
ATANBgkqhkiG9w0BAQsFAAOCAQEARAcOL0Y1XBYqIT/ySRFmN6f+cLUO3sPGllt8
BLYhHsnyJjzV4By00GLcLp5cd14sIfkyVPPFA7kCwOGbL52avRo6+bPB2Bdg6MRt
wbXG3pa6DQXQ2vsZ0I1bXUdCS05YbfvfTrF7LLNCPYbul4Wph5zT360JmBVLKPaX
smw8fAPhdDwHix1ee2bopldrPrS0L55t3HLOBEF4XT9TCXFS23yBpujGsLEwHgaJ
x1un6v2v+bEPr8tpPv33WlSC9Fwlit0Xwf6sp/YuX11t223D7QmGN8rRyqv9Fm5l
RZh2a6rJjlnErdcLx/+5ojsCjbElfluJvsToc+iCcwut6FKcPg==
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
TEST_ATTESTATION = (
    b'\x1f\x8b\x08\x08\xb9\xe37`\x00\x03attestation.dat\x00\x01\x08\x01\xf7'
    b'\xfecontent\n>\xede\xeb\xd3\x9d\x9e\x8e*\xa2\xf4\x04i\xec\x10lI\xa1\xc5'
    b'\xd6\x0c\xfd\x1a^T\x1f&>f\xb2\xae}UD\xf1\xbaW\xcf\xec\xc5\x10\x86s\x92A'
    b'\xa1E\xc3\xf9=8/\xe5\xf4y\xf1\xa4H\xb1"\x08\xe7\x1a\xd1[\xc2\xb1CCO\x82'
    b'\xe7-\xbd-=u\x15\x9a=\x1b\x98\xec\xb6\x1d\xc0\xd2\xf7\xcb\x99g\xdd\xed'
    b'\xba\xcb\x9bK\xc7\xd8[\xd9\xf8?K\x0f\xd5\xaaO\xd4R0\xf6>\x18\xb2F\x13 '
    b'\xedi\xedV\xdc\x1bR-j\x85\xe3\xd5\x92\x9a\x9dU4\xc8\x13\xa10\xbbg\xee'
    b'\xa3R\x8a\xcf\x88\x91p\xde\x9c\xe1\x82\xcd\x8a>\xa0\x1c\xf2\xb5\xb2\xb2'
    b'\x91.Z\t\xc8a{\x896\x03+|\x8b\xa0\xb7\x16\xe8E\xca\x0c+\x17)\xd4\xd2s'
    b'\x96\xfen\xa9\xf7\xa2\x1eW\xd3\xbd\n\x16\x12\xea8\xaa\x85xJ\x13d\xe5\x85'
    b'\xdd\xe6\xca\x82;qw\xbe\x8fa\xb7\xeb\x06L\xd2\\pb\x0b\xbf\x9bj\xcc\xb0'
    b'\x92\xf2\x81v\x1c\xa0\xa3?{~\x8e\xc1O\x1a\xc9\x7f\x9cCH\x1d\xef\x85\xe1'
    b'\xeb\xa5\x08\x01\x00\x00')


def test_verify_certificate():
    signing_cert = x509.load_pem_x509_certificate(TEST_OWNER_ROOT,
                                                  backends.default_backend())
    issued_cert = x509.load_pem_x509_certificate(TEST_OWNER_PARTITION_CHAIN,
                                                 backends.default_backend())
    assert verify_attestation_chains.verify_certificate(signing_cert,
                                                        issued_cert)


def test_verify_certificate_fail():
    signing_cert = x509.load_pem_x509_certificate(TEST_OWNER_ROOT,
                                                  backends.default_backend())
    issued_cert = x509.load_pem_x509_certificate(TEST_MANUFACTURER_ROOT,
                                                 backends.default_backend())
    assert not verify_attestation_chains.verify_certificate(signing_cert,
                                                            issued_cert)


def get_test_manufacturer_root():
    return x509.load_pem_x509_certificate(TEST_MANUFACTURER_ROOT,
                                          backends.default_backend())


def get_test_owner_root():
    return x509.load_pem_x509_certificate(TEST_OWNER_ROOT,
                                          backends.default_backend())


def make_temporary_file(contents):
    """Creates a NamedTemporaryFile with contents and returns its file name.

    Args:
        contents: The contents to write to the temporary file.

    Returns:
        The name of the temporary file.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(contents)
    temp_file.close()
    return temp_file.name


@pytest.fixture(scope='function')
def test_data():
    mfr_root = make_temporary_file(TEST_MANUFACTURER_ROOT)
    mfr_chain = make_temporary_file(TEST_MANUFACTURER_CHAIN)
    owner_root = make_temporary_file(TEST_OWNER_ROOT)
    owner_card_chain = make_temporary_file(TEST_OWNER_CARD_CHAIN)
    owner_partition_chain = make_temporary_file(TEST_OWNER_PARTITION_CHAIN)
    cert_chains = make_temporary_file(b'\n'.join([
        TEST_MANUFACTURER_CHAIN,
        TEST_OWNER_CARD_CHAIN,
        TEST_OWNER_PARTITION_CHAIN
    ]))
    attestation = make_temporary_file(TEST_ATTESTATION)

    param = {
        'mfr_root': mfr_root,
        'mfr_chain': mfr_chain,
        'owner_root': owner_root,
        'owner_card_chain': owner_card_chain,
        'owner_partition_chain': owner_partition_chain,
        'cert_chains': cert_chains,
        'attestation': attestation
    }
    yield param


def test_verify(monkeypatch, test_data):
    monkeypatch.setattr(verify_attestation_chains,
                        'MANUFACTURER_CERT_SUBJECT_BYTES',
                        TEST_MANUFACTURER_SUBJECT_BYTES)
    monkeypatch.setattr(verify_attestation_chains,
                        'get_manufacturer_root_certificate',
                        get_test_manufacturer_root)
    monkeypatch.setattr(verify_attestation_chains,
                        'get_owner_root_certificate',
                        get_test_owner_root)
    assert verify_attestation_chains.verify(test_data['cert_chains'],
                                            test_data['attestation'])


def test_verify_invalid_mfr_root_fails(monkeypatch, test_data):
    monkeypatch.setattr(verify_attestation_chains,
                        'MANUFACTURER_CERT_SUBJECT_BYTES',
                        b'invalid')
    monkeypatch.setattr(verify_attestation_chains,
                        'get_manufacturer_root_certificate',
                        get_test_owner_root)
    monkeypatch.setattr(verify_attestation_chains,
                        'get_owner_root_certificate',
                        get_test_owner_root)

    assert not verify_attestation_chains.verify(test_data['cert_chains'],
                                                test_data['attestation'])
