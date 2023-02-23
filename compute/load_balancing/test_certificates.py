#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os
from pathlib import Path
import time
import uuid

from googleapiclient import discovery
import pytest
from pytest import fixture

from create_certificate import create_certificate
from create_regional_certificate import create_regional_certificate

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
CERTIFICATE_FILE = Path(__file__).parent / "test_fixtures" / "certificate.pem"
PRIVATE_KEY_FILE = Path(__file__).parent / "test_fixtures" / "test_key.pem"


@fixture(scope="module")
def api_service():
    service = discovery.build("compute", "v1")
    yield service


@fixture
def autodelete_certificate_name(api_service):
    cert_name = "test-certificate-" + uuid.uuid4().hex[:10]

    yield cert_name

    api_service.sslCertificates().delete(
        project=PROJECT_ID, sslCertificate=cert_name
    ).execute()


@fixture
def autodelete_regional_certificate_name(api_service):
    cert_name = "test-certificate-" + uuid.uuid4().hex[:10]

    yield cert_name, "europe-west2"

    api_service.regionSslCertificates().delete(
        project=PROJECT_ID, sslCertificate=cert_name, region="europe-west2"
    ).execute()


def test_global_register(api_service, autodelete_certificate_name):
    create_certificate(
        PROJECT_ID, CERTIFICATE_FILE, PRIVATE_KEY_FILE, autodelete_certificate_name
    )
    time.sleep(2)
    certificates = api_service.sslCertificates().list(project=PROJECT_ID).execute()
    for certificate in certificates["items"]:
        if certificate["name"] == autodelete_certificate_name:
            break
    else:
        pytest.fail("Certificate wasn't created.")


def test_regional_register(api_service, autodelete_regional_certificate_name):
    certificate_name, region_name = autodelete_regional_certificate_name

    create_regional_certificate(
        PROJECT_ID, region_name, CERTIFICATE_FILE, PRIVATE_KEY_FILE, certificate_name
    )
    time.sleep(2)
    certificates = (
        api_service.regionSslCertificates()
        .list(project=PROJECT_ID, region=region_name)
        .execute()
    )
    for certificate in certificates["items"]:
        if certificate["name"] == certificate_name:
            break
    else:
        pytest.fail("Certificate wasn't created.")
