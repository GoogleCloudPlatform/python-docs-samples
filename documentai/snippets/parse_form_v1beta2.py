# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License");
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

# [START documentai_parse_form_beta]
from google.cloud import documentai_v1beta2 as documentai


def parse_form(
    project_id="YOUR_PROJECT_ID",
    input_uri="gs://cloud-samples-data/documentai/form.pdf",
):
    """Parse a form"""

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        gcs_source=gcs_source, mime_type="application/pdf"
    )

    # Improve form parsing results by providing key-value pair hints.
    # For each key hint, key is text that is likely to appear in the
    # document as a form field name (i.e. "DOB").
    # Value types are optional, but can be one or more of:
    # ADDRESS, LOCATION, ORGANIZATION, PERSON, PHONE_NUMBER, ID,
    # NUMBER, EMAIL, PRICE, TERMS, DATE, NAME
    key_value_pair_hints = [
        documentai.types.KeyValuePairHint(
            key="Emergency Contact", value_types=["NAME"]
        ),
        documentai.types.KeyValuePairHint(key="Referred By"),
    ]

    # Setting enabled=True enables form extraction
    form_extraction_params = documentai.types.FormExtractionParams(
        enabled=True, key_value_pair_hints=key_value_pair_hints
    )

    # Location can be 'us' or 'eu'
    parent = "projects/{}/locations/us".format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config,
        form_extraction_params=form_extraction_params,
    )

    document = client.process_document(request=request)

    def _get_text(el):
        """Doc AI identifies form fields by their offsets
        in document text. This function converts offsets
        to text snippets.
        """
        response = ""
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        for segment in el.text_anchor.text_segments:
            start_index = segment.start_index
            end_index = segment.end_index
            response += document.text[start_index:end_index]
        return response

    for page in document.pages:
        print("Page number: {}".format(page.page_number))
        for form_field in page.form_fields:
            print(
                "Field Name: {}\tConfidence: {}".format(
                    _get_text(form_field.field_name), form_field.field_name.confidence
                )
            )
            print(
                "Field Value: {}\tConfidence: {}".format(
                    _get_text(form_field.field_value), form_field.field_value.confidence
                )
            )


# [END documentai_parse_form_beta]
