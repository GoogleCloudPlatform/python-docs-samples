# Copyright 2019 Google LLC
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
from unittest import mock
import uuid

from apache_beam.io.gcp.gcsio import GcsIO
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.test_stream import TestStream
from apache_beam.testing.test_utils import TempDir
from apache_beam.transforms.window import TimestampedValue


import PubSubToGCS

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
UUID = uuid.uuid1().hex


@mock.patch("apache_beam.Pipeline", TestPipeline)
@mock.patch(
    "apache_beam.io.ReadFromPubSub",
    lambda topic: (
        TestStream()
        .advance_watermark_to(0)
        .advance_processing_time(30)
        .add_elements([TimestampedValue(b"a", 1575937195)])
        .advance_processing_time(30)
        .add_elements([TimestampedValue(b"b", 1575937225)])
        .advance_processing_time(30)
        .add_elements([TimestampedValue(b"c", 1575937255)])
        .advance_watermark_to_infinity()
    ),
)
def test_pubsub_to_gcs():
    PubSubToGCS.run(
        input_topic="unused",  # mocked by TestStream
        output_path=f"gs://{BUCKET}/pubsub/{UUID}/output",
        window_size=1,  # 1 minute
        num_shards=1,
        pipeline_args=[
            "--project",
            PROJECT,
            "--temp_location",
            TempDir().get_path(),
        ],
    )

    # Check for output files on GCS.
    gcs_client = GcsIO()
    files = gcs_client.list_prefix(f"gs://{BUCKET}/pubsub/{UUID}")
    assert len(files) > 0

    # Clean up.
    gcs_client.delete_batch(list(files))
