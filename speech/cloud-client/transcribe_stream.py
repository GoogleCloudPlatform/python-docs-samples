#!/usr/bin/env python

# author: Yogesh Garg
# email: yogeshg91@gmail.com
# github: yogeshg

"""Google Cloud Speech API sample application for transcribing audio streams

Example usage:
    python transcribe_stream resources/audio.raw
 
sources:
 * https://googlecloudplatform.github.io/google-cloud-python/stable/speech-usage.html#streaming-recognition

"""

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from google.cloud import speech

SAMPLE_RATE=16000
speech_client = speech.Client()

def transcribe_stream(stream):
    logging.debug('{} is closed: {}'.format(str(stream), stream.closed))

    sample = speech_client.sample( stream=stream,
                                    encoding=speech.Encoding.LINEAR16,
                                    sample_rate=SAMPLE_RATE)
    results = list(sample.streaming_recognize())
    print 'results len:{}'
    for r in results:
        for a in r.alternatives:
            print a.confidence, a.transcript

def main(args):
    with open(args.filename, 'rb') as stream:
        transcribe_stream( stream )

def parse_args():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename', type=str)
    args = p.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main( args )

