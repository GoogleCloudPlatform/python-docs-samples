#!/usr/bin/env python

# Copyright 2016 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START full_tutorial_script]
# [START import_libraries]
import argparse
import io

import googleapiclient.discovery
# [END import_libraries]


def print_sentiment(filename):
    """Prints sentiment analysis on a given file contents."""
    # [START authenticating_to_the_api]
    service = googleapiclient.discovery.build('language', 'v1')
    # [END authenticating_to_the_api]

    # [START constructing_the_request]
    with io.open(filename, 'r') as review_file:
        review_file_contents = review_file.read()

    service_request = service.documents().analyzeSentiment(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': review_file_contents,
            }
        }
    )
    response = service_request.execute()
    # [END constructing_the_request]

    # [START parsing_the_response]
    score = response['documentSentiment']['score']
    magnitude = response['documentSentiment']['magnitude']

    for n, sentence in enumerate(response['sentences']):
        sentence_sentiment = sentence['sentiment']['score']
        print('Sentence {} has a sentiment score of {}'.format(n,
              sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
            score, magnitude))
    # [END parsing_the_response]


# [START running_your_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'movie_review_filename',
        help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()
    print_sentiment(args.movie_review_filename)
# [END running_your_application]
# [END full_tutorial_script]
