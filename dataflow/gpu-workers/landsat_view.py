import base64
import logging
import os
import re
from io import BytesIO

import numpy as np
import rasterio as rio
import tensorflow as tf
from PIL import Image

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


DEFAULT_RGB_BANDS = ['B4', 'B3', 'B2']
DEFAULT_MIN_BAND_VALUE = 0.0
DEFAULT_MAX_BAND_VALUE = 12000.0
DEFAULT_GAMMA = 0.5

DEFAULT_SCENES = [
    'LC08_L1TP_115078_20200608_20200625_01_T1',  # Western Australia
    'LC08_L1TP_203045_20200108_20200114_01_T1',  # Eye of the Sahara
    'LC08_L1TP_001067_20200727_20200807_01_T1',  # Amazon
    'LC08_L1TP_169034_20200720_20200807_01_T1',  # Lake Urmia, Iran
    'LC08_L1TP_110036_20191009_20191018_01_T1',  # Japan
    'LC08_L1TP_170059_20200101_20200113_01_T1',  # Mount Elgon, Uganda
    'LC08_L1TP_045031_20200715_20200722_01_T1',  # Mount Shasta, California
    'LC08_L1TP_137045_20200211_20200225_01_T1',  # Ganges river delta
    'LC08_L1TP_037035_20191212_20191212_01_T1',  # Grand canyon
    'LC08_L1TP_019046_20191214_20191226_01_T1',  # Yucatan peninsula
    'LC08_L1TP_019024_20190621_20190704_01_T1',  # Nottaway river, Quebec
    'LC08_L1TP_135040_20190314_20190325_01_T1',  # Arunachal Pradesh
    'LC08_L1TP_119038_20191109_20191115_01_T1',  # Lake Tai, China
    'LC08_L1TP_073087_20200516_20200527_01_T1',  # New Zealand
    'LC08_L1TP_163042_20200608_20200625_01_T1',  # Bahrain
    'LC08_L1TP_176039_20200603_20200608_01_T1',  # Cairo, Egypt
    'LC08_L1TP_195028_20200116_20200127_01_T1',  # Swiss Alps
    'LC08_L1TP_161028_20200525_20200608_01_T1',  # Barsakelmes Reserve, Kazakhstan
    'LC08_L1TP_178069_20200804_20200821_01_T1',  # Angola
]

SCENE_RE = re.compile(
    r'(?P<sensor>L[COTEM]0[78])_'
    r'(?P<correction_level>L1TP|L1GT|L1GS)_'
    r'(?P<wrs_path>\d\d\d)'
    r'(?P<wrs_row>\d\d\d)_'
    r'(?P<year>\d\d\d\d)'
    r'(?P<month>\d\d)'
    r'(?P<day>\d\d)_'
    r'(?P<processing_year>\d\d\d\d)'
    r'(?P<processing_month>\d\d)'
    r'(?P<processing_day>\d\d)_'
    r'(?P<collection>\d\d)_'
    r'(?P<category>RT|T1|T2)')


def get_valid_band_paths(scene, bands):
    try:
        return [get_band_path(scene, band) for band in bands]
    except Exception as e:
        # If it fails, don't crash the entire pipeline.
        # Instead, log the error and skip this scene.
        logging.error(e, exc_info=True)
        return []


def get_band_path(scene, band):
    # Extract the metadata from the scene ID using a regular expression.
    m = SCENE_RE.match(scene)
    if m:
        g = m.groupdict()
        scene_dir = 'gs://gcp-public-data-landsat/{}/{}/{}/{}/{}'.format(
            g['sensor'], g['collection'], g['wrs_path'], g['wrs_row'], scene)

        path = '{}/{}_{}.TIF'.format(scene_dir, scene, band)
        if not tf.io.gfile.exists(path):
            raise ValueError(
                'failed to load band "{}", GCS path not found: {}'.format(band, path))

        logging.info('{}: get_band_path({}): {}'.format(scene, band, path))
        return scene, (band, path)

    raise ValueError('invalid scene ID: {}'.format(scene))


def load_band(scene, band_path):
    band, path = band_path

    # Use rasterio to read the GeoTIFF values from Cloud Storage.
    with tf.io.gfile.GFile(path, 'rb') as f, rio.open(f) as data:
        logging.info('{}: load_band({})'.format(scene, band))
        return scene, (band, data.read(1))


def preprocess_pixels(scene, values, min_value=0.0, max_value=1.0, gamma=1.0):
    values = tf.cast(values, dtype=tf.float32)
    logging.info('{}: preprocess_pixels({}, min={}, max={}, gamma={})'
                 .format(scene, values.shape, min_value, max_value, gamma))

    # Make sure we have a GPU available.
    gpu_devices = tf.config.list_physical_devices('GPU')
    logging.info('GPU devices: {}'.format(gpu_devices))
    if len(gpu_devices) == 0:
        logging.warning('No GPUs found, defaulting to CPU')

    # Reshape (band, width, height) into (width, height, band).
    pixels = tf.transpose(values, (1, 2, 0))

    # Rescale to values from 0.0 to 1.0 and clamp them into that range.
    pixels -= min_value
    pixels /= max_value
    pixels = tf.clip_by_value(pixels, 0.0, 1.0)

    # Apply gamma correction.
    pixels **= 1.0 / gamma

    # Return the pixel values as int8 in the range from 0 to 255,
    # which is what PIL.Image expects.
    return scene, tf.cast(pixels * 255.0, dtype=tf.uint8)


def save_to_gcs(scene, image, output_path_prefix, format='JPEG'):
    filename = os.path.join(output_path_prefix, scene + '.' + format.lower())
    with beam.io.gcp.gcsio.GcsIO().open(filename, 'w') as f:
        image.save(f, format)


def run(scenes, output_path_prefix, vis_params, beam_args=None):
    bands = vis_params['bands']
    min_value = vis_params['min']
    max_value = vis_params['max']
    gamma = vis_params['gamma']

    options = PipelineOptions(beam_args, save_main_session=True)
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | 'Create scene IDs' >> beam.Create(scenes)
            | 'Get band paths' >> beam.FlatMap(get_valid_band_paths, bands)
            | 'Load bands' >> beam.MapTuple(load_band)
            | 'Group bands per scene' >> beam.GroupByKey()
            | 'Combine bands to dict' >> beam.MapTuple(
                lambda scene, bands: (scene, dict(bands)))
            | 'Create RGB pixels' >> beam.MapTuple(
                lambda scene, bands: (scene, [bands[b] for b in bands]))
            | 'Preprocess pixels' >> beam.MapTuple(
                preprocess_pixels, min_value, max_value, gamma)
            | 'Convert to image' >> beam.MapTuple(
                lambda scene, rgb_pixels:
                (scene, Image.fromarray(rgb_pixels.numpy(), mode='RGB')))
            | 'Save to Cloud Storage' >> beam.MapTuple(
                save_to_gcs, output_path_prefix)
        )


if __name__ == '__main__':
    import argparse

    logging.basicConfig(level=logging.INFO)
    logging.getLogger(
        'apache_beam.runners.dataflow.internal.apiclient').setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--scene',
        # required=True,
        default=DEFAULT_SCENES,
    )
    parser.add_argument(
        '--output-path-prefix',
        required=True,
        # default='gs://dcavazos-lyra/samples/dataflow/landsat_images/',
    )
    parser.add_argument(
        '--bands',
        default=DEFAULT_RGB_BANDS,
    )
    parser.add_argument(
        '--min',
        default=DEFAULT_MIN_BAND_VALUE,
    )
    parser.add_argument(
        '--max',
        default=DEFAULT_MAX_BAND_VALUE
    )
    parser.add_argument(
        '--gamma',
        default=DEFAULT_GAMMA,
    )
    args, beam_args = parser.parse_known_args()

    vis_params = {
        'bands': args.bands,
        'min': args.min,
        'max': args.max,
        'gamma': args.gamma,
    }
    run(args.scene, args.output_path_prefix, vis_params, beam_args)
