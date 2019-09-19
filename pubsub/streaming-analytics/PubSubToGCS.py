import argparse
import datetime
import logging

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions


class ProcessDoFn(beam.DoFn):
    """A distributed processing function that acts on individual elements in
    the PCollection.
    """

    def process(self, element, publish_time=beam.DoFn.TimestampParam):
        """Enrich each Pub/Sub message with its publish timestamps.

        Args:
            element (bytestring): Pub/Sub message.
            publish_time: Default to the publish timestamp from Pub/Sub.

        Yields:
            str: Message body and publish timestamp.
        """
        publish_time = datetime.datetime.utcfromtimestamp(
            float(publish_time)).strftime("%Y-%m-%d %H:%M:%S.%f")
        yield element.decode('utf-8') + ' published at ' + publish_time


class OutputDoFn(beam.DoFn):

    def __init__(self, output_path):
        self.output_path = output_path

    def process(self, batch, window=beam.DoFn.WindowParam):
        """Write each batch in its own file to a Google Cloud Storage bucket.

        Args:
            batch (list of bytestring): list of enriched Pub/Sub messages.
            window: Window info that has been bound to each batch.
        """

        ts_format = '%H:%M'
        window_start = window.start.to_utc_datetime().strftime(ts_format)
        window_end = window.end.to_utc_datetime().strftime(ts_format)
        filename = '-'.join([self.output_path, window_start, window_end])
        contents = '\n'.join(str(element) for element in batch)

        with beam.io.gcp.gcsio.GcsIO().open(filename=filename, mode='w') as f:
            f.write(contents.encode('utf-8'))


class ApplyWindowing(beam.PTransform):
    """A composite transform that enriches Pub/Sub messages by their publish
    timestamps and groups them by timed windows.
    """

    def __init__(self, window_size):
        # Convert minutes into seconds.
        self.window_size = int(window_size * 60)

    def expand(self, pcoll):
        return (pcoll
                # Assigns each element in the PCollection to a time interval.
                | beam.WindowInto(window.FixedWindows(self.window_size))
                # Add publish timestamps to each element.
                | 'Process Pub/Sub Message' >> beam.ParDo(ProcessDoFn())
                | 'Add Empty Key' >> beam.Map(lambda elem: (None, elem))
                | 'Groupby' >> beam.GroupByKey()
                | 'Remove Key' >> beam.MapTuple(lambda key, val: val))


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic',
        help=('The Cloud Pub/Sub topic to read from.'
              '"projects/<PROJECT_NAME>/topics/<TOPIC_NAME>".'))
    parser.add_argument(
        '--window_size',
        type=float,
        default=1.0,
        help=('Output file\'s window size in number of minutes.'))
    parser.add_argument(
        '--output_path',
        help=('GCS Path of the output file including filename prefix.'))
    known_args, pipeline_args = parser.parse_known_args(argv)

    # `save_main_session` is True because one or more DoFn's rely on
    # globally imported modules.
    pipeline_options = PipelineOptions(pipeline_args,
                                       streaming=True,
                                       save_main_session=True)

    with beam.Pipeline(options=pipeline_options) as pipeline:
        (pipeline
         | 'Read PubSub Messages' >> beam.io.ReadFromPubSub(
             topic=known_args.input_topic)
         | 'Window into' >> ApplyWindowing(known_args.window_size)
         | 'Write to GCS' >> beam.ParDo(OutputDoFn(known_args.output_path)))


if __name__ == '__main__': # noqa
    logging.getLogger().setLevel(logging.INFO)
    run()
