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


def get_dataset(project_id, dataset_id):
    """Get a dataset."""
    # [START automl_translate_get_dataset]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'YOUR_PROJECT_ID'
    # dataset_id = 'YOUR_DATASET_ID'

    client = automl.AutoMlClient()
    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(
        project_id, 'us-central1', dataset_id
    )
    dataset = client.get_dataset(dataset_full_id)

    # Display the dataset information
    print(u'Dataset name: {}'.format(dataset.name))
    print(u'Dataset id: {}'.format(dataset.name.split('/')[-1]))
    print(u'Dataset display name: {}'.format(dataset.display_name))
    print('Dataset create time:')
    print(u'\tseconds: {}'.format(dataset.create_time.seconds))
    print(u'\tnanos: {}'.format(dataset.create_time.nanos))
    print('Translation dataset metadata:')
    print(
        u'\tsource_language_code: {}'.format(
            dataset.translation_dataset_metadata.source_language_code
        )
    )
    print(
        u'\ttarget_language_code: {}'.format(
            dataset.translation_dataset_metadata.target_language_code
        )
    )
    # [END automl_translate_get_dataset]
