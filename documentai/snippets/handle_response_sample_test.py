# # Copyright 2020 Google LLC
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
#

# flake8: noqa

import os

from documentai.snippets import handle_response_sample


def test_process_document_ocr(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "52a38e080c1a7296"
    processor_version = "rc"
    file_path = "resources/handwritten_form.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_ocr_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    assert "Page 1" in out
    assert "en" in out
    assert "FakeDoc" in out


def test_process_document_form(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "90484cfdedb024f6"
    processor_version = "stable"
    file_path = "resources/invoice.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_form_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "There are 1 page(s) in this document.",
        "Table with 4 columns and 6 rows",
        "Found 13 form field(s)",
        "'BALANCE DUE': '$2140.00'",
    ]
    for expected_string in expected_strings:
        assert expected_string in out


def test_process_document_quality(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "7fcb597c523721b3"
    processor_version = "stable"
    poor_quality_file_path = "resources/document_quality_poor.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_quality_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=poor_quality_file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "Page 1 has a quality score of",
        "defect_blurry score of 9",
        "defect_noisy",
    ]
    for expected_string in expected_strings:
        assert expected_string in out


def test_process_document_specialized(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "feacd98c28866ede"
    processor_version = "stable"
    file_path = "resources/us_driver_license.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_specialized_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "Document Id",
        "97551579",
    ]
    for expected_string in expected_strings:
        assert expected_string in out


def test_process_document_splitter(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "ed55eeb2b276066f"
    processor_version = "stable"
    file_path = "resources/multi_document.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_splitter_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    # Remove newlines and quotes from output for easier comparison
    out = out.replace(' "" ', " ").replace("\n", "")

    expected_strings = [
        "Found 8 subdocuments",
        "confident that pages 1, 2 are a subdocument",
        "confident that page 10 is a subdocument",
    ]
    for expected_string in expected_strings:
        assert expected_string in out
