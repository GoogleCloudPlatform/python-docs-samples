#!/usr/bin/env python

# Copyright 2019 Google LLC
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


def predict(project_id, model_id, content):
    """Predict."""
    # [START automl_language_entity_extraction_predict]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'YOUR_PROJECT_ID'
    # model_id = 'YOUR_MODEL_ID'
    # content = 'text to predict'

    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = prediction_client.model_path(
        project_id, 'us-central1', model_id
    )

    text_snippet = automl.types.TextSnippet(
        content=content,
        mime_type='text/plain')  # Types: 'text/plain', 'text/html'
    payload = automl.types.ExamplePayload(text_snippet=text_snippet)

    response = prediction_client.predict(model_full_id, payload)

    for annotation_payload in response.payload:
        print(u'Text Extract Entity Types: {}'.format(
            annotation_payload.display_name))
        print(u'Text Score: {}'.format(
            annotation_payload.text_extraction.score))
        text_segment = annotation_payload.text_extraction.text_segment
        print(u'Text Extract Entity Content: {}'.format(text_segment.content))
        print(u'Text Start Offset: {}'.format(text_segment.start_offset))
        print(u'Text End Offset: {}'.format(text_segment.end_offset))
    # [END automl_language_entity_extraction_predict]
