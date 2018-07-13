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
import shutil
import tempfile

import pytest

import deid

HARMFUL_STRING = 'My SSN is 372819127'
HARMLESS_STRING = 'My favorite color is blue'
GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')
WRAPPED_KEY = ('CiQAz0hX4+go8fJwn80Fr8pVImwx+tmZdqU7JL+7TN/S5JxBU9gSSQDhFHpFVy'
               'uzJps0YH9ls480mU+JLG7jI/0lL04i6XJRWqmI6gUSZRUtECYcLH5gXK4SXHlL'
               'rotx7Chxz/4z7SIpXFOBY61z0/U=')
KEY_NAME = ('projects/python-docs-samples-tests/locations/global/keyRings/'
            'dlp-test/cryptoKeys/dlp-test')
SURROGATE_TYPE = 'SSN_TOKEN'
CSV_FILE = os.path.join(os.path.dirname(__file__), 'resources/dates.csv')
DATE_SHIFTED_AMOUNT = 30
DATE_FIELDS = ['birth_date', 'register_date']
CSV_CONTEXT_FIELD = 'name'


@pytest.fixture(scope='module')
def tempdir():
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


def test_deidentify_with_mask(capsys):
    deid.deidentify_with_mask(GCLOUD_PROJECT, HARMFUL_STRING,
                              ['US_SOCIAL_SECURITY_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'My SSN is *********' in out


def test_deidentify_with_mask_ignore_insensitive_data(capsys):
    deid.deidentify_with_mask(GCLOUD_PROJECT, HARMLESS_STRING)

    out, _ = capsys.readouterr()
    assert HARMLESS_STRING in out


def test_deidentify_with_mask_masking_character_specified(capsys):
    deid.deidentify_with_mask(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ['US_SOCIAL_SECURITY_NUMBER'],
        masking_character='#')

    out, _ = capsys.readouterr()
    assert 'My SSN is #########' in out


def test_deidentify_with_mask_masking_number_specified(capsys):
    deid.deidentify_with_mask(GCLOUD_PROJECT, HARMFUL_STRING,
                              ['US_SOCIAL_SECURITY_NUMBER'],
                              number_to_mask=7)

    out, _ = capsys.readouterr()
    assert 'My SSN is *******27' in out


def test_deidentify_with_fpe(capsys):
    deid.deidentify_with_fpe(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ['US_SOCIAL_SECURITY_NUMBER'],
        alphabet='NUMERIC',
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME)

    out, _ = capsys.readouterr()
    assert 'My SSN is' in out
    assert '372819127' not in out


def test_deidentify_with_fpe_uses_surrogate_info_types(capsys):
    deid.deidentify_with_fpe(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ['US_SOCIAL_SECURITY_NUMBER'],
        alphabet='NUMERIC',
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
        surrogate_type=SURROGATE_TYPE)

    out, _ = capsys.readouterr()
    assert 'My SSN is SSN_TOKEN' in out
    assert '372819127' not in out


def test_deidentify_with_fpe_ignores_insensitive_data(capsys):
    deid.deidentify_with_fpe(
        GCLOUD_PROJECT,
        HARMLESS_STRING,
        alphabet='NUMERIC',
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME)

    out, _ = capsys.readouterr()
    assert HARMLESS_STRING in out


def test_deidentify_with_date_shift(tempdir, capsys):
    output_filepath = os.path.join(tempdir, 'dates-shifted.csv')

    deid.deidentify_with_date_shift(
        GCLOUD_PROJECT,
        input_csv_file=CSV_FILE,
        output_csv_file=output_filepath,
        lower_bound_days=DATE_SHIFTED_AMOUNT,
        upper_bound_days=DATE_SHIFTED_AMOUNT,
        date_fields=DATE_FIELDS)

    out, _ = capsys.readouterr()

    assert 'Successful' in out


def test_deidentify_with_date_shift_using_context_field(tempdir, capsys):
    output_filepath = os.path.join(tempdir, 'dates-shifted.csv')

    deid.deidentify_with_date_shift(
        GCLOUD_PROJECT,
        input_csv_file=CSV_FILE,
        output_csv_file=output_filepath,
        lower_bound_days=DATE_SHIFTED_AMOUNT,
        upper_bound_days=DATE_SHIFTED_AMOUNT,
        date_fields=DATE_FIELDS,
        context_field_id=CSV_CONTEXT_FIELD,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME)

    out, _ = capsys.readouterr()

    assert 'Successful' in out


def test_reidentify_with_fpe(capsys):
    labeled_fpe_string = 'My SSN is SSN_TOKEN(9):731997681'

    deid.reidentify_with_fpe(
        GCLOUD_PROJECT,
        labeled_fpe_string,
        surrogate_type=SURROGATE_TYPE,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
        alphabet='NUMERIC')

    out, _ = capsys.readouterr()

    assert '731997681' not in out
