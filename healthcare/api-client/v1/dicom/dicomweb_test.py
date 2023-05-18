# Copyright 2018 Google LLC All Rights Reserved.
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

import os
import sys
import uuid

import backoff
from googleapiclient.errors import HttpError
import pytest

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "datasets"))  # noqa
import datasets  # noqa
import dicom_stores  # noqa
import dicomweb  # noqa

location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

dataset_id = f"test_dataset-{uuid.uuid4()}"
dicom_store_id = f"test_dicom_store_{uuid.uuid4()}"

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
dcm_file_name = "dicom_00000001_000.dcm"
dcm_file = os.path.join(RESOURCES, dcm_file_name)
# The study_uid, series_uid, and instance_uid are not assigned by the
# server and are part of the metadata of dcm_file
study_uid = "1.3.6.1.4.1.11129.5.5.111396399361969898205364400549799252857604"
series_uid = "1.3.6.1.4.1.11129.5.5.195628213694300498946760767481291263511724"
instance_uid = "{}.{}".format(
    "1.3.6.1.4.1.11129.5.5", "153751009835107614666834563294684339746480"
)


@pytest.fixture(scope="module")
def test_dataset():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        try:
            datasets.create_dataset(project_id, location, dataset_id)
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(f"Got exception {err.resp.status} while creating dataset")
            else:
                raise

    create()

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            datasets.delete_dataset(project_id, location, dataset_id)
        except HttpError as err:
            # The API returns 403 when the dataset doesn't exist.
            if err.resp.status == 403:
                print(f"Got exception {err.resp.status} while deleting dataset")
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def test_dicom_store():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        try:
            dicom_stores.create_dicom_store(
                project_id, location, dataset_id, dicom_store_id
            )
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(
                    "Got exception {} while creating DICOM store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    create()

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            dicom_stores.delete_dicom_store(
                project_id, location, dataset_id, dicom_store_id
            )
        except HttpError as err:
            # The API returns 404 when the DICOM store doesn't exist.
            # The API returns 403 when the dataset doesn't exist, so
            # if we try to delete a DICOM store when the parent dataset
            # doesn't exist, the server will return a 403.
            if err.resp.status == 404 or err.resp.status == 403:
                print(
                    "Got exception {} while deleting DICOM store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    clean_up()


def test_dicomweb_store_instance(test_dataset, test_dicom_store, capsys):
    dicomweb.dicomweb_store_instance(
        project_id, location, dataset_id, dicom_store_id, dcm_file
    )

    out, _ = capsys.readouterr()

    # Check that store instance worked
    assert "Stored DICOM instance" in out


def test_dicomweb_search_instance_studies(test_dataset, test_dicom_store, capsys):
    dicomweb.dicomweb_store_instance(
        project_id, location, dataset_id, dicom_store_id, dcm_file
    )

    dicomweb.dicomweb_search_instance(project_id, location, dataset_id, dicom_store_id)

    dicomweb.dicomweb_search_studies(project_id, location, dataset_id, dicom_store_id)

    out, _ = capsys.readouterr()

    # Check that search instance worked
    assert "Instances:" in out
    # Check that search studies worked
    assert "Studies found: response is <Response [204]>" in out


def test_dicomweb_retrieve_study(test_dataset, test_dicom_store, capsys):
    try:
        dicomweb.dicomweb_store_instance(
            project_id, location, dataset_id, dicom_store_id, dcm_file
        )

        dicomweb.dicomweb_retrieve_study(
            project_id, location, dataset_id, dicom_store_id, study_uid
        )

        # Assert study was downloaded
        assert os.path.isfile("study.multipart")

        out, _ = capsys.readouterr()

        # Check that retrieve study worked
        assert "Retrieved study" in out

    finally:
        # Delete downloaded study
        os.remove("study.multipart")


def test_dicomweb_retrieve_instance(test_dataset, test_dicom_store, capsys):
    try:
        dicomweb.dicomweb_store_instance(
            project_id, location, dataset_id, dicom_store_id, dcm_file
        )

        dicomweb.dicomweb_retrieve_instance(
            project_id,
            location,
            dataset_id,
            dicom_store_id,
            study_uid,
            series_uid,
            instance_uid,
        )

        # Assert instance was downloaded
        assert os.path.isfile("instance.dcm")

        out, _ = capsys.readouterr()

        # Check that retrieve instance worked
        assert "Retrieved DICOM instance" in out

    finally:
        # Delete downloaded instance
        os.remove("instance.dcm")


def test_dicomweb_retrieve_rendered(test_dataset, test_dicom_store, capsys):
    try:
        dicomweb.dicomweb_store_instance(
            project_id, location, dataset_id, dicom_store_id, dcm_file
        )

        dicomweb.dicomweb_retrieve_rendered(
            project_id,
            location,
            dataset_id,
            dicom_store_id,
            study_uid,
            series_uid,
            instance_uid,
        )

        # Assert rendered image was downloaded
        assert os.path.isfile("rendered_image.png")

        out, _ = capsys.readouterr()

        # Check that retrieve rendered image worked
        assert "Retrieved rendered image" in out

    finally:
        # Delete downloaded rendered image
        os.remove("rendered_image.png")


def test_dicomweb_delete_study(test_dataset, test_dicom_store, capsys):
    dicomweb.dicomweb_store_instance(
        project_id, location, dataset_id, dicom_store_id, dcm_file
    )

    dicomweb.dicomweb_delete_study(
        project_id, location, dataset_id, dicom_store_id, study_uid
    )

    out, _ = capsys.readouterr()

    # Check that store instance worked
    assert "Deleted study." in out
