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

import deid

harmful_string = 'My SSN is 372819127'
parent = os.environ['GCLOUD_PROJECT']
wrapped_key = os.environ['DLP_DEID_WRAPPED_KEY']
key_name = os.environ['DLP_DEID_KEY_NAME']
surrogate_type = 'SSN_TOKEN'
csv_file = 'resources/dates.csv'
output_csv_file = 'resources/temp.results.csv'
date_shifted_amount = 30
date_fields = ['birth_date', 'register_date']
csv_context_field = 'name'


# [START Deidentify with masking]
def test_deidentify_with_mask(capsys):
    harmful_string = 'My SSN is 372819127'

    deid.deidentify_with_mask(parent, harmful_string)

    out, _ = capsys.readouterr()
    assert 'My SSN is *********' in out


def test_deidentify_with_mask_ignore_insensitive_data(capsys):
    harmless_string = 'My favorite color is blue'

    deid.deidentify_with_mask(parent, harmless_string)

    out, _ = capsys.readouterr()
    assert harmless_string in out


def test_deidentify_with_mask_masking_character_specified(capsys):
    harmful_string = 'My SSN is 372819127'

    deid.deidentify_with_mask(parent, harmful_string, masking_character='#')

    out, _ = capsys.readouterr()
    assert 'My SSN is #########' in out


def test_deidentify_with_mask_masking_number_specified(capsys):
    harmful_string = 'My SSN is 372819127'

    deid.deidentify_with_mask(parent, harmful_string, number_to_mask=7)

    out, _ = capsys.readouterr()
    assert 'My SSN is *******27' in out


def test_deidentify_with_mask_handles_masking_number_error(capsys):
    harmful_string = 'My SSN is 372819127'

    deid.deidentify_with_mask(parent, harmful_string, number_to_mask=-3)

    out, _ = capsys.readouterr()
    assert 'My SSN is *********' in out
# [END deidentify_with_mask]


# [START Deidentify with FPE]
def test_deidentify_with_fpe(capsys):
    harmful_string = 'My SSN is 372819127'

    deid.deidentify_with_fpe(parent, harmful_string, alphabet='NUMERIC',
                             wrapped_key=wrapped_key, key_name=key_name)

    out, _ = capsys.readouterr()
    assert 'My SSN is' in out
    assert '372819127' not in out


def test_deidentify_with_fpe_uses_surrogate_info_types(capsys):
    harmful_string = 'My SSN is 372819127'

    deid.deidentify_with_fpe(parent, harmful_string, alphabet='NUMERIC',
                             wrapped_key=wrapped_key, key_name=key_name,
                             surrogate_type=surrogate_type)

    out, _ = capsys.readouterr()
    assert 'My SSN is SSN_TOKEN' in out
    assert '372819127' not in out


def test_deidentify_with_fpe_ignores_insensitive_data(capsys):
    harmless_string = 'My favorite color is blue'

    deid.deidentify_with_fpe(parent, harmless_string, alphabet='NUMERIC',
                             wrapped_key=wrapped_key, key_name=key_name)

    out, _ = capsys.readouterr()
    assert harmless_string in out
# [END Deidentify with FPE]


# [START Deidentify with date shift]
def test_deidentify_with_date_shift(capsys):
    deid.deidentify_with_date_shift(parent, input_csv_file=csv_file,
                                    output_csv_file=output_csv_file,
                                    lower_bound_days=date_shifted_amount,
                                    upper_bound_days=date_shifted_amount,
                                    date_fields=date_fields)

    out, _ = capsys.readouterr()

    assert 'Successful' in out
    # read in csv??


def test_deidentify_with_date_shift_using_context_field(capsys):
    deid.deidentify_with_date_shift(parent, input_csv_file=csv_file,
                                    output_csv_file=output_csv_file,
                                    lower_bound_days=date_shifted_amount,
                                    upper_bound_days=date_shifted_amount,
                                    date_fields=date_fields,
                                    context_field_id=csv_context_field,
                                    wrapped_key=wrapped_key,
                                    key_name=key_name)

    out, _ = capsys.readouterr()

    assert 'Successful' in out


def test_deidentify_with_date_shift_requires_all_fields():
    with pytest.raises(StandardError):
        deid.deidentify_with_date_shift(parent, input_csv_file=csv_file,
                                        output_csv_file=output_csv_file,
                                        lower_bound_days=date_shifted_amount,
                                        upper_bound_days=date_shifted_amount,
                                        date_fields=date_fields,
                                        context_field_id=csv_context_field,
                                        key_name=key_name)
# [END Deidentify with date shift]


# [START Reidentify with FPE]
def test_reidentify_with_fpe(capsys):
    labeled_fpe_string = 'My SSN is SSN_TOKEN(9):731997681'

    deid.reidentify_with_fpe(parent, labeled_fpe_string,
                             surrogate_type=surrogate_type,
                             wrapped_key=wrapped_key, key_name=key_name,
                             alphabet='NUMERIC')

    out, _ = capsys.readouterr()

    assert harmful_string in out
# [END Reidentify with FPE]
