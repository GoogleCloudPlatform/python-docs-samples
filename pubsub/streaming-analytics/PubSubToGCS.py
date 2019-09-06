import argparse
import logging

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions


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
    p = beam.Pipeline(options=pipeline_options)

    # Read from Cloud Pub/Sub into a PCollection.
    if known_args.input_topic:
        messages = (p
                    | 'Read Pub/Sub Messages' >> beam.io.ReadFromPubSub(
                        topic=known_args.input_topic)
                    .with_output_types(bytes))

    # Group messages by fixed-sized minute intervals.
    transformed = (messages
                   | beam.WindowInto(
                       window.FixedWindows(known_args.window_size))
                   .with_output_types(bytes))

    # Output to GCS
    transformed | beam.io.WriteToText(file_path_prefix=known_args.output_path)

    result = p.run()
    result.wait_until_finish()

if __name__ == '__main__': # noqa
    logging.getLogger().setLevel(logging.INFO)
    run()
