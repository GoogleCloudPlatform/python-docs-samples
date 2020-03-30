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


# [START documentai_analyze_form]
from google.cloud import documentai_v1beta2 as documentai

def analyze_form(project_id='YOUR_PROJECT_ID', input_uri='gs://cloud-samples-data/documentai/invoice.pdf'):
    """Parse a form"""

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = types.GcsSource(uri=input_uri)
    input_config = types.InputConfig(
        gcs_source=gcs_source, mime_type='application/pdf')

    # Improve form parsing results by providing key-value pair hints.
    # For each key hint, key is text that is likely to appear in the
    # document as a form field name (i.e. "DOB").
    # Value types are optional, but can be one or more of:
    # ADDRESS, LOCATION, ORGANIZATION, PERSON, PHONE_NUMBER, ID,
    # NUMBER, EMAIL, PRICE, TERMS, DATE, NAME
    key_value_pair_hints = [
        types.KeyValuePairHint(key='Name', value_types=['NAME']),
        types.KeyValuePairHint(key='Agreement Number', value_types=['NUMBER'])
    ]

    # Setting enabled=True enables form extraction
    form_extraction_params = types.FormExtractionParams(
        enabled=True, key_value_pair_hints=key_value_pair_hints)

    # For now, location must be us-central1
    parent = "projects/{}/locations/us-central1".format(project_id)
    request = types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config,
        form_extraction_params=form_extraction_params)

    return client.process_document(request=request)
    # [END analyze_form]


def parse_form_response(document):
    """Parse Document response from the DAI API to make
    it easier to work with. Returns:

    [
        {'name':
            {'text': 'Address: ',
            'start_index': 746,
            'end_index': 755,
            'confidence': 1.0,
            'bounding_poly':
                [x: 0.12581700086593628
                y: 0.31313130259513855
                , x: 0.19771242141723633
                y: 0.31313130259513855
                , x: 0.19771242141723633
                y: 0.32575756311416626
                , x: 0.12581700086593628
                y: 0.32575756311416626]
        },
        'value':
            {'text': '100 Franklin Street, Mountain View, CA, 94035\n',
            'start_index': 755,
            'end_index': 801,
            'confidence': 1.0,
            'bounding_poly':
                [x: 0.2222222238779068
                y: 0.31439393758773804
                , x: 0.5947712659835815
                y: 0.31439393758773804
                , x: 0.5947712659835815
                y: 0.32702019810676575
                , x: 0.2222222238779068
                y: 0.32702019810676575
                ]
        },
        'page': 0},
    ...
    ]
     """
    # [START parse_form_response]
    form_items = []
    for page_num, page in enumerate(document.pages):
        for form_field in page.form_fields:
            form_item = {}
            field_name = form_field.field_name
            start_idx = field_name.text_anchor.text_segments[0].start_index
            end_idx = field_name.text_anchor.text_segments[0].end_index
            form_item["name"] = {
                "text": document.text[start_idx:end_idx],
                "start_index": start_idx,
                "end_index": end_idx,
                "confidence": field_name.confidence,
                "bounding_poly": field_name.bounding_poly.normalized_vertices

            }

            field_value = form_field.field_value
            start_idx = field_value.text_anchor.text_segments[0].start_index
            end_idx = field_value.text_anchor.text_segments[0].end_index
            form_item["value"] = {
                "text": document.text[start_idx:end_idx],
                "start_index": start_idx,
                "end_index": end_idx,
                "confidence": field_value.confidence,
                "bounding_poly": field_value.bounding_poly.normalized_vertices
            }

            form_item["page"] = page_num
            form_items.append(form_item)
    return form_items
    # [END parse_form_response]
