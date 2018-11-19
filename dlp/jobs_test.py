# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest

import jobs

GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')
TEST_COLUMN_NAME = 'zip_code'
TEST_TABLE_PROJECT_ID = 'bigquery-public-data'
TEST_DATASET_ID = 'san_francisco'
TEST_TABLE_ID = 'bikeshare_trips'


@pytest.fixture(scope='session')
def create_test_job():
    import google.cloud.dlp
    dlp = google.cloud.dlp.DlpServiceClient()

    parent = dlp.project_path(GCLOUD_PROJECT)

    # Construct job request
    risk_job = {
        'privacy_metric': {
            'categorical_stats_config': {
                'field': {
                    'name': TEST_COLUMN_NAME
                }
            }
        },
        'source_table': {
            'project_id': TEST_TABLE_PROJECT_ID,
            'dataset_id': TEST_DATASET_ID,
            'table_id': TEST_TABLE_ID
        }
    }

    response = dlp.create_dlp_job(parent, risk_job=risk_job)
    full_path = response.name
    # API expects only job name, not full project path
    job_name = full_path[full_path.rfind('/')+1:]
    return job_name


def test_list_dlp_jobs(capsys):
    jobs.list_dlp_jobs(GCLOUD_PROJECT)

    out, _ = capsys.readouterr()
    assert 'Job: projects/' in out


def test_list_dlp_jobs_with_filter(capsys):
    jobs.list_dlp_jobs(GCLOUD_PROJECT, filter_string='state=DONE')

    out, _ = capsys.readouterr()
    assert 'Job: projects/' in out


def test_list_dlp_jobs_with_job_type(capsys):
    jobs.list_dlp_jobs(GCLOUD_PROJECT, job_type='INSPECT_JOB')

    out, _ = capsys.readouterr()
    assert 'Job: projects/' in out


def test_delete_dlp_job(capsys):
    test_job_name = create_test_job()
    jobs.delete_dlp_job(GCLOUD_PROJECT, test_job_name)
