# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START pubsub_to_gcs]
import argparse
import datetime
import json
import logging

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions


class GroupWindowsIntoBatches(beam.PTransform):
    """A composite transform that groups Pub/Sub messages based on publish
    time and outputs a list of dictionaries, where each contains one message
    and its publish timestamp.
    """

    def __init__(self, window_size):
        # Convert minutes into seconds.
        self.window_size = int(window_size * 60)

    def expand(self, pcoll):
        return (pcoll
                # Assigns window info to each Pub/Sub message based on its
                # publish timestamp.
                | beam.WindowInto(window.FixedWindows(self.window_size))
                | 'Process Pub/Sub Message' >> (beam.ParDo(AddTimestamps()))
                # Use a dummy key to group the elements in the same window.
                | 'Add Dummy Key' >> beam.Map(lambda elem: (None, elem))
                | 'Groupby' >> beam.GroupByKey()
                | 'Abandon Dummy Key' >> beam.MapTuple(lambda _, val: val))


class AddTimestamps(beam.DoFn):

    def process(self, element, publish_time=beam.DoFn.TimestampParam):
        """Processes each incoming windowed element by extracting the Pub/Sub
        message body and its publish timestamp into a dictionary.
        `publish_time` defaults to the publish timestamp returned by the
        Pub/Sub server and is accessible by Beam at runtime.
        """

        yield {
            'message_body': json.loads(element),
            'publish_time': datetime.datetime.utcfromtimestamp(
                float(publish_time)).strftime("%Y-%m-%d %H:%M:%S.%f"),
        }


class WriteBatchesToGCS(beam.DoFn):

    def __init__(self, output_path):
        self.output_path = output_path

    def process(self, batch, window=beam.DoFn.WindowParam):
        """Write one batch per file to a Google Cloud Storage bucket. """

        ts_format = '%H:%M'
        window_start = window.start.to_utc_datetime().strftime(ts_format)
        window_end = window.end.to_utc_datetime().strftime(ts_format)
        filename = '-'.join([self.output_path, window_start, window_end])

        with beam.io.gcp.gcsio.GcsIO().open(filename=filename, mode='w') as f:
            f.write(json.dumps(batch).encode('utf-8'))


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic',
        help='The Cloud Pub/Sub topic to read from.\n'
             '"projects/<PROJECT_NAME>/topics/<TOPIC_NAME>".')
    parser.add_argument(
        '--window_size',
        type=float,
        default=1.0,
        help='Output file\'s window size in number of minutes.')
    parser.add_argument(
        '--output_path',
        help='GCS Path of the output file including filename prefix.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # `save_main_session` is set to true because one or more DoFn's rely on
    # globally imported modules.
    pipeline_options = PipelineOptions(
        pipeline_args, streaming=True, save_main_session=True)

    with beam.Pipeline(options=pipeline_options) as pipeline:
        (pipeline
         | 'Read PubSub Messages' >> beam.io.ReadFromPubSub(
             topic=known_args.input_topic)
         | 'Window into' >> GroupWindowsIntoBatches(known_args.window_size)
         | 'Write to GCS' >> beam.ParDo(
             WriteBatchesToGCS(known_args.output_path)))


if __name__ == '__main__': # noqa
    logging.getLogger().setLevel(logging.INFO)
    run()
# [END pubsub_to_gcs]
