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
from documentai.snippets import handle_response_sample_v1beta3


def test_process_document_ocr(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "52a38e080c1a7296"
    processor_version = "pretrained-ocr-v2.0-2023-06-02"
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

    # Document Quality
    assert "Quality score" in out

    # Font Detection
    assert "Font Size" in out
    assert "Handwritten" in out

    # Checkbox Detection
    file_path = "resources/checkbox.png"
    mime_type = "image/png"

    handle_response_sample.process_document_ocr_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    assert "unfilled_checkbox" in out
    assert "filled_checkbox" in out


def test_process_document_ocr_checkbox(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "52a38e080c1a7296"
    processor_version = "pretrained-ocr-v2.0-2023-06-02"
    file_path = "resources/checkbox.png"
    mime_type = "image/png"

    handle_response_sample.process_document_ocr_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    assert "unfilled_checkbox" in out
    assert "filled_checkbox" in out


def test_process_document_form():
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "90484cfdedb024f6"
    processor_version = "pretrained-form-parser-v2.0-2022-11-10"
    file_path = "resources/invoice.pdf"
    mime_type = "application/pdf"

    document = handle_response_sample.process_document_form_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )

    assert len(document.pages) == 1
    assert len(document.pages[0].tables[0].header_rows[0].cells) == 4
    assert len(document.pages[0].tables[0].body_rows) == 6
    assert len(document.entities) > 0


def test_process_document_quality(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "52a38e080c1a7296"
    processor_version = "pretrained-ocr-v2.0-2023-06-02"
    poor_quality_file_path = "resources/document_quality_poor.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_ocr_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=poor_quality_file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "Quality score",
        "defect_blurry",
        "defect_noisy",
    ]
    for expected_string in expected_strings:
        assert expected_string in out


def test_process_document_entity_extraction(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "feacd98c28866ede"
    processor_version = "stable"
    file_path = "resources/us_driver_license.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_entity_extraction_sample(
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


def test_process_document_summarizer(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "a2ab373924245a07"
    processor_version = "pretrained-foundation-model-v1.1-2023-09-12"
    file_path = "resources/superconductivity.pdf"
    mime_type = "application/pdf"

    handle_response_sample_v1beta3.process_document_summarizer_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "Superconductivity",
    ]
    for expected_string in expected_strings:
        assert expected_string in out


def test_process_document_layout():
    document = handle_response_sample.process_document_layout_sample(
        project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
        location="us",
        processor_id="85b02a52f356f564",
        processor_version="pretrained",
        file_path="resources/superconductivity.pdf",
        mime_type="application/pdf",
    )

    assert document
    assert document.document_layout
    assert document.chunked_document


def test_process_document_custom_extractor(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    processor_id = "295e41049f27a2fa"
    processor_version = "pretrained-foundation-model-v1.0-2023-08-22"
    file_path = "resources/invoice.pdf"
    mime_type = "application/pdf"

    handle_response_sample.process_document_custom_extractor_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = ["invoice_id", "001"]
    for expected_string in expected_strings:
        assert expected_string in out
