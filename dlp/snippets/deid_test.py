# Copyright 2023 Google LLC
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

import google.cloud.dlp_v2
import pytest

import deid

HARMFUL_STRING = "My SSN is 372819127"
HARMLESS_STRING = "My favorite color is blue"
GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
UNWRAPPED_KEY = "YWJjZGVmZ2hpamtsbW5vcA=="
WRAPPED_KEY = (
    "CiQAz0hX4+go8fJwn80Fr8pVImwx+tmZdqU7JL+7TN/S5JxBU9gSSQDhFHpFVy"
    "uzJps0YH9ls480mU+JLG7jI/0lL04i6XJRWqmI6gUSZRUtECYcLH5gXK4SXHlL"
    "rotx7Chxz/4z7SIpXFOBY61z0/U="
)
KEY_NAME = (
    f"projects/{GCLOUD_PROJECT}/locations/global/keyRings/"
    "dlp-test/cryptoKeys/dlp-test"
)
SURROGATE_TYPE = "SSN_TOKEN"
CSV_FILE = os.path.join(os.path.dirname(__file__), "resources/dates.csv")
DATE_SHIFTED_AMOUNT = 30
DATE_FIELDS = ["birth_date", "register_date"]
CSV_CONTEXT_FIELD = "name"
TABULAR_DATA = {
    "header": ["age", "patient", "happiness_score"],
    "rows": [
        ["101", "Charles Dickens", "95"],
        ["22", "Jane Austen", "21"],
        ["90", "Mark Twain", "75"]
    ]
}


@pytest.fixture(scope="module")
def tempdir():
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


def test_deidentify_with_mask(capsys):
    deid.deidentify_with_mask(
        GCLOUD_PROJECT, HARMFUL_STRING, ["US_SOCIAL_SECURITY_NUMBER"]
    )

    out, _ = capsys.readouterr()
    assert "My SSN is *********" in out


def test_deidentify_with_mask_ignore_insensitive_data(capsys):
    deid.deidentify_with_mask(
        GCLOUD_PROJECT, HARMLESS_STRING, ["US_SOCIAL_SECURITY_NUMBER"]
    )

    out, _ = capsys.readouterr()
    assert HARMLESS_STRING in out


def test_deidentify_with_mask_masking_character_specified(capsys):
    deid.deidentify_with_mask(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        masking_character="#",
    )

    out, _ = capsys.readouterr()
    assert "My SSN is #########" in out


def test_deidentify_with_mask_masking_number_specified(capsys):
    deid.deidentify_with_mask(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        number_to_mask=7,
    )

    out, _ = capsys.readouterr()
    assert "My SSN is *******27" in out


def test_deidentify_with_redact(capsys):
    deid.deidentify_with_redact(
        GCLOUD_PROJECT, HARMFUL_STRING + "!", ["US_SOCIAL_SECURITY_NUMBER"]
    )
    out, _ = capsys.readouterr()
    assert "My SSN is !" in out


def test_deidentify_with_replace(capsys):
    deid.deidentify_with_replace(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        replacement_str="REPLACEMENT_STR",
    )

    out, _ = capsys.readouterr()
    assert "My SSN is REPLACEMENT_STR" in out


def test_deidentify_with_fpe(capsys):
    deid.deidentify_with_fpe(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        alphabet=google.cloud.dlp_v2.CharsToIgnore.CommonCharsToIgnore.NUMERIC,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
    )

    out, _ = capsys.readouterr()
    assert "My SSN is" in out
    assert "372819127" not in out


def test_deidentify_with_deterministic(capsys):
    deid.deidentify_with_deterministic(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        surrogate_type=SURROGATE_TYPE,
        key_name=KEY_NAME,
        wrapped_key=WRAPPED_KEY,
    )

    out, _ = capsys.readouterr()
    assert "My SSN is" in out
    assert "372819127" not in out


def test_deidentify_with_fpe_uses_surrogate_info_types(capsys):
    deid.deidentify_with_fpe(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        alphabet=google.cloud.dlp_v2.CharsToIgnore.CommonCharsToIgnore.NUMERIC,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
        surrogate_type=SURROGATE_TYPE,
    )

    out, _ = capsys.readouterr()
    assert "My SSN is SSN_TOKEN" in out
    assert "372819127" not in out


def test_deidentify_with_fpe_ignores_insensitive_data(capsys):
    deid.deidentify_with_fpe(
        GCLOUD_PROJECT,
        HARMLESS_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        alphabet=google.cloud.dlp_v2.CharsToIgnore.CommonCharsToIgnore.NUMERIC,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
    )

    out, _ = capsys.readouterr()
    assert HARMLESS_STRING in out


def test_deidentify_with_date_shift(tempdir, capsys):
    output_filepath = os.path.join(tempdir, "dates-shifted.csv")

    deid.deidentify_with_date_shift(
        GCLOUD_PROJECT,
        input_csv_file=CSV_FILE,
        output_csv_file=output_filepath,
        lower_bound_days=DATE_SHIFTED_AMOUNT,
        upper_bound_days=DATE_SHIFTED_AMOUNT,
        date_fields=DATE_FIELDS,
    )

    out, _ = capsys.readouterr()

    assert "Successful" in out


def test_deidentify_with_date_shift_using_context_field(tempdir, capsys):
    output_filepath = os.path.join(tempdir, "dates-shifted.csv")

    deid.deidentify_with_date_shift(
        GCLOUD_PROJECT,
        input_csv_file=CSV_FILE,
        output_csv_file=output_filepath,
        lower_bound_days=DATE_SHIFTED_AMOUNT,
        upper_bound_days=DATE_SHIFTED_AMOUNT,
        date_fields=DATE_FIELDS,
        context_field_id=CSV_CONTEXT_FIELD,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
    )

    out, _ = capsys.readouterr()

    assert "Successful" in out


def test_reidentify_with_fpe(capsys):
    labeled_fpe_string = "My SSN is SSN_TOKEN(9):731997681"

    deid.reidentify_with_fpe(
        GCLOUD_PROJECT,
        labeled_fpe_string,
        surrogate_type=SURROGATE_TYPE,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
        alphabet=google.cloud.dlp_v2.CharsToIgnore.CommonCharsToIgnore.NUMERIC,
    )

    out, _ = capsys.readouterr()

    assert "731997681" not in out


def test_reidentify_with_deterministic(capsys):
    labeled_fpe_string = "My SSN is SSN_TOKEN(36):ATeRUd3WWnAHHFtjtl1bv+CT09FZ7hyqNas="

    deid.reidentify_with_deterministic(
        GCLOUD_PROJECT,
        labeled_fpe_string,
        surrogate_type=SURROGATE_TYPE,
        key_name=KEY_NAME,
        wrapped_key=WRAPPED_KEY,
    )

    out, _ = capsys.readouterr()

    assert "SSN_TOKEN(" not in out


def test_deidentify_free_text_with_fpe_using_surrogate(capsys):
    labeled_fpe_string = "My phone number is 4359916732"

    deid.deidentify_free_text_with_fpe_using_surrogate(
        GCLOUD_PROJECT,
        labeled_fpe_string,
        info_type="PHONE_NUMBER",
        surrogate_type="PHONE_TOKEN",
        unwrapped_key=UNWRAPPED_KEY,
        alphabet=google.cloud.dlp_v2.CharsToIgnore.CommonCharsToIgnore.NUMERIC,
    )

    out, _ = capsys.readouterr()

    assert "PHONE_TOKEN" in out
    assert "My phone number is" in out
    assert "4359916732" not in out


def test_reidentify_free_text_with_fpe_using_surrogate(capsys):
    labeled_fpe_string = "My phone number is PHONE_TOKEN(10):9617256398"

    deid.reidentify_free_text_with_fpe_using_surrogate(
        GCLOUD_PROJECT,
        labeled_fpe_string,
        surrogate_type="PHONE_TOKEN",
        unwrapped_key=UNWRAPPED_KEY,
        alphabet=google.cloud.dlp_v2.CharsToIgnore.CommonCharsToIgnore.NUMERIC,
    )

    out, _ = capsys.readouterr()

    assert "PHONE_TOKEN" not in out
    assert "9617256398" not in out
    assert "My phone number is" in out


def test_deidentify_with_replace_infotype(capsys):
    url_to_redact = "https://cloud.google.com"
    deid.deidentify_with_replace_infotype(
        GCLOUD_PROJECT,
        "My favorite site is " + url_to_redact,
        ["URL"],
    )

    out, _ = capsys.readouterr()

    assert url_to_redact not in out
    assert "My favorite site is [URL]" in out


def test_deidentify_with_exception_list(capsys):
    content_str = "jack@example.org accessed record of user: gary@example.org"
    exception_list = ["jack@example.org", "jill@example.org"]
    deid.deidentify_with_exception_list(
        GCLOUD_PROJECT,
        content_str,
        ["EMAIL_ADDRESS"],
        exception_list
    )

    out, _ = capsys.readouterr()

    assert "gary@example.org" not in out
    assert "jack@example.org accessed record of user: [EMAIL_ADDRESS]" in out


def test_deidentify_table_condition_masking(capsys):
    deid_list = ["happiness_score"]
    deid.deidentify_table_condition_masking(
        GCLOUD_PROJECT,
        TABULAR_DATA,
        deid_list,
        condition_field="age",
        condition_operator="GREATER_THAN",
        condition_value=89,
    )
    out, _ = capsys.readouterr()
    assert "string_value: \"**\"" in out
    assert "string_value: \"21\"" in out


def test_deidentify_table_condition_masking_with_masking_character_specified(capsys):
    deid_list = ["happiness_score"]
    deid.deidentify_table_condition_masking(
        GCLOUD_PROJECT,
        TABULAR_DATA,
        deid_list,
        condition_field="age",
        condition_operator="GREATER_THAN",
        condition_value=89,
        masking_character="#"
    )
    out, _ = capsys.readouterr()
    assert "string_value: \"##\"" in out
    assert "string_value: \"21\"" in out
