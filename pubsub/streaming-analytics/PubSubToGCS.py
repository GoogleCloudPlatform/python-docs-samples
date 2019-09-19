import argparse
import datetime
import logging

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions


class ProcessDoFn(beam.DoFn):
    def process(self, element, publish_time=beam.DoFn.TimestampParam):
        publish_time = datetime.datetime.utcfromtimestamp(
            float(publish_time)).strftime("%Y-%m-%d %H:%M:%S.%f")
        yield element.decode('utf-8') + ' published at ' + publish_time


class CustomDoFn(beam.DoFn):
    def __init__(self, output_path):
        self.output_path = output_path

    def process(self, batch, window=beam.DoFn.WindowParam):
        ts_format = '%Y-%m-%d %H:%M:%S'
        window_start = window.start.to_utc_datetime().strftime(ts_format)
        window_end = window.end.to_utc_datetime().strftime(ts_format)
        filename = self.output_path + ' ' + window_start + ' to ' + window_end
        contents = '\n'.join(str(element) for element in batch)

        with beam.io.gcp.gcsio.GcsIO().open(filename=filename, mode='w') as f:
            f.write(contents.encode('utf-8'))


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic',
        help=('The Cloud Pub/Sub topic to read from.'
              '"projects/<PROJECT_NAME>/topics/<TOPIC_NAME>".'))
    parser.add_argument(
        '--window_size',
        type=int,
        default=1,
        help=('Output file\'s window size in number of minutes.'))
    parser.add_argument(
        '--output_path',
        help=('GCS Path of the output file including filename prefix.'))
    known_args, pipeline_args = parser.parse_known_args(argv)

    # One or more DoFn's rely on global context.
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as p:
        (p
            | 'Read Pub/Sub Messages' >> beam.io.ReadFromPubSub(
                topic=known_args.input_topic)
            | beam.WindowInto(window.FixedWindows(known_args.window_size*60))
            | beam.ParDo(ProcessDoFn())
            | beam.Map(lambda e: (None, e))
            | beam.GroupByKey()
            | beam.MapTuple(lambda k, v: v)
            | 'Write to GCS' >> beam.ParDo(CustomDoFn(known_args.output_path)))

if __name__ == '__main__': # noqa
    logging.getLogger().setLevel(logging.INFO)
    run()
