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

from gcp_devrel.testing.flaky import flaky
import google.cloud.pubsub

import pytest

import risk

GCLOUD_PROJECT = 'nodejs-docs-samples'
TABLE_PROJECT = 'nodejs-docs-samples'
TOPIC_ID = 'dlp-test'
SUBSCRIPTION_ID = 'dlp-test-subscription'
DATASET_ID = 'integration_tests_dlp'
UNIQUE_FIELD = 'Name'
REPEATED_FIELD = 'Mystery'
NUMERIC_FIELD = 'Age'
STRING_BOOLEAN_FIELD = 'Gender'


# Create new custom topic/subscription
@pytest.fixture(scope='module')
def topic_id():
    # Creates a pubsub topic, and tears it down.
    publisher = google.cloud.pubsub.PublisherClient()
    topic_path = publisher.topic_path(GCLOUD_PROJECT, TOPIC_ID)
    try:
        publisher.create_topic(topic_path)
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield TOPIC_ID

    publisher.delete_topic(topic_path)


@pytest.fixture(scope='module')
def subscription_id(topic_id):
    # Subscribes to a topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    topic_path = subscriber.topic_path(GCLOUD_PROJECT, topic_id)
    subscription_path = subscriber.subscription_path(
        GCLOUD_PROJECT, SUBSCRIPTION_ID)
    try:
        subscriber.create_subscription(subscription_path, topic_path)
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield SUBSCRIPTION_ID

    subscriber.delete_subscription(subscription_path)


@flaky
def test_numerical_risk_analysis(topic_id, subscription_id, capsys):
    risk.numerical_risk_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        NUMERIC_FIELD,
        topic_id,
        subscription_id)

    out, _ = capsys.readouterr()
    assert 'Value Range:' in out


@flaky
def test_categorical_risk_analysis_on_string_field(
        topic_id, subscription_id, capsys):
    risk.categorical_risk_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        UNIQUE_FIELD,
        topic_id,
        subscription_id, timeout=180)

    out, _ = capsys.readouterr()
    assert 'Most common value occurs' in out


@flaky
def test_categorical_risk_analysis_on_number_field(
        topic_id, subscription_id, capsys):
    risk.categorical_risk_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        NUMERIC_FIELD,
        topic_id,
        subscription_id)

    out, _ = capsys.readouterr()
    assert 'Most common value occurs' in out


@flaky
def test_k_anonymity_analysis_single_field(topic_id, subscription_id, capsys):
    risk.k_anonymity_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        topic_id,
        subscription_id,
        [NUMERIC_FIELD])

    out, _ = capsys.readouterr()
    assert 'Quasi-ID values:' in out
    assert 'Class size:' in out


@flaky
def test_k_anonymity_analysis_multiple_fields(topic_id, subscription_id,
                                              capsys):
    risk.k_anonymity_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        topic_id,
        subscription_id,
        [NUMERIC_FIELD, REPEATED_FIELD])

    out, _ = capsys.readouterr()
    assert 'Quasi-ID values:' in out
    assert 'Class size:' in out


@flaky
def test_l_diversity_analysis_single_field(topic_id, subscription_id, capsys):
    risk.l_diversity_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        topic_id,
        subscription_id,
        UNIQUE_FIELD,
        [NUMERIC_FIELD])

    out, _ = capsys.readouterr()
    assert 'Quasi-ID values:' in out
    assert 'Class size:' in out
    assert 'Sensitive value' in out


@flaky
def test_l_diversity_analysis_multiple_field(
        topic_id, subscription_id, capsys):
    risk.l_diversity_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        topic_id,
        subscription_id,
        UNIQUE_FIELD,
        [NUMERIC_FIELD, REPEATED_FIELD])

    out, _ = capsys.readouterr()
    assert 'Quasi-ID values:' in out
    assert 'Class size:' in out
    assert 'Sensitive value' in out


@flaky
def test_k_map_estimate_analysis_single_field(
        topic_id, subscription_id, capsys):
    risk.k_map_estimate_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        topic_id,
        subscription_id,
        [NUMERIC_FIELD],
        ['AGE'])

    out, _ = capsys.readouterr()
    assert 'Anonymity range:' in out
    assert 'Size:' in out
    assert 'Values' in out


@flaky
def test_k_map_estimate_analysis_multiple_field(
        topic_id, subscription_id, capsys):
    risk.k_map_estimate_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        DATASET_ID,
        'harmful',
        topic_id,
        subscription_id,
        [NUMERIC_FIELD, STRING_BOOLEAN_FIELD],
        ['AGE', 'GENDER'])

    out, _ = capsys.readouterr()
    assert 'Anonymity range:' in out
    assert 'Size:' in out
    assert 'Values' in out


@flaky
def test_k_map_estimate_analysis_quasi_ids_info_types_equal(
        topic_id, subscription_id):
    with pytest.raises(ValueError):
        risk.k_map_estimate_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            DATASET_ID,
            'harmful',
            topic_id,
            subscription_id,
            [NUMERIC_FIELD, STRING_BOOLEAN_FIELD],
            ['AGE'])
