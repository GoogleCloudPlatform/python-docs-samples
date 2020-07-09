# Lint as: python3
"""Tests for quickstartv2."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pytest
import uuid
from google3.testing.pybase import googletest
import quickstartv2

import access
import service_accounts

# Setting up variables for testing
GCLOUD_PROJECT = os.environ["GCLOUD_PROJECT"]

@pytest.fixture(scope="module")
def test_member():
    # section to create service account to test policy updates.
    # we use the first portion of uuid4 because full version is too long.
    name = "python-test-" + str(uuid.uuid4()).split('-')[0]
    email = name + "@" + GCLOUD_PROJECT + ".iam.gserviceaccount.com"
    member = "serviceAccount:" + email
    service_accounts.create_service_account(
        GCLOUD_PROJECT, name, "Py Test Account"
    )

    yield member

    # deleting the service account created above
    service_accounts.delete_service_account(email)

def test_quickstartv2(capsys):
    quickstartv2.quickstart()
    out, _ = capsys.readouterr()
    assert 'Title' in out

def test_quickstartv2_initialize_service(capsys):
    quickstartv2.initialize_service()
    out, _ = capsys.readouterr()
    print(out)