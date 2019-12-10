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

import logging
import os
import unittest
import uuid

import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.test_stream import TestStream
from apache_beam.testing.test_utils import TempDir
from apache_beam.transforms.window import TimestampedValue
from apache_beam.testing.util import assert_that

from PubSubToGCS import *

PROJECT = os.environ["GCLOUD_PROJECT"]
BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
UUID = uuid.uuid1().hex


class PubSubToGCSTest(unittest.TestCase):
    def test_pubsub_to_gcs(self):

        pipeline_options = PipelineOptions(
            project=PROJECT,
            runner="DirectRunner",
            temp_location=TempDir().get_path(),
            streaming=True,
            save_main_session=True,
        )

        with TestPipeline(options=pipeline_options) as p:

            mocked_pubsub_stream = (
                TestStream()
                .advance_watermark_to(0)
                .advance_processing_time(30)
                .add_elements([TimestampedValue(b"a", 1575937195)])
                .advance_processing_time(30)
                .add_elements([TimestampedValue(b"b", 1575937225)])
                .advance_processing_time(30)
                .add_elements([TimestampedValue(b"c", 1575937255)])
                .advance_watermark_to_infinity()
            )

            output_path = "gs://{}/pubsub/{}/output".format(BUCKET, UUID)

            _ = (
                p
                | mocked_pubsub_stream
                | "Window into" >> GroupWindowsIntoBatches(1)
                | "Write to GCS" >> beam.ParDo(WriteBatchesToGCS(output_path))
            )

        # Check for output files on GCS.
        gcs_client = beam.io.gcp.gcsio.GcsIO()
        files = gcs_client.list_prefix("gs://{}/pubsub/{}".format(BUCKET, UUID))
        assert len(files) > 0

        # Clean up.
        gcs_client.delete_batch(list(files))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
