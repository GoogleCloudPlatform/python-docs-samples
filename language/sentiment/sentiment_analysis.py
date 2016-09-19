# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Demonstrates how to make a simple call to the Natural Language API'''

import argparse
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def main(movie_review_filename):
    '''Run a sentiment analysis request on text within a passed filename.'''

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('language', 'v1beta1', credentials=credentials)

    with open(movie_review_filename, 'r') as review_file:
        service_request = service.documents().analyzeSentiment(
            body={
                'document': {
                    'type': 'PLAIN_TEXT',
                    'content': review_file.read(),
                }
            }
        )
        response = service_request.execute()

    polarity = response['documentSentiment']['polarity']
    magnitude = response['documentSentiment']['magnitude']

    print('Sentiment: polarity of {} with magnitude of {}'.format(
        polarity, magnitude))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'movie_review_filename',
        help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()
    main(args.movie_review_filename)
