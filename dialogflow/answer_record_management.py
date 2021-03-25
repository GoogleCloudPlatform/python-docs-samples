#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Dialogflow API Python sample showing how to manage AnswerRecord.
"""

from google.cloud import dialogflow_v2beta1 as dialogflow


# [START dialogflow_update_answer_record]
def update_answer_record(project_id, answer_record_id, is_clicked):
    """Update the answer record.

    Args:
        project_id: The GCP project linked with the conversation profile.
        answer_record_id: The answer record id returned along with the
        suggestion.
        is_clicked: whether the answer record is clicked."""

    client = dialogflow.AnswerRecordsClient()
    answer_record_path = client.answer_record_path(project_id,
                                                   answer_record_id)

    response = client.update_answer_record(
        answer_record={
            'name': answer_record_path,
            'answer_feedback': {
                'clicked': is_clicked
            }
        },
        update_mask={'paths': ['answer_feedback']})
    print('AnswerRecord Name: {}'.format(response.name))
    print('Clicked: {}'.format(response.answer_feedback.clicked))
    return response


# [END dialogflow_update_answer_record]
