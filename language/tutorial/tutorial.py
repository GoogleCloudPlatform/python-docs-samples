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
import argparse


from googleapiclient import discovery


from oauth2client.client import GoogleCredentials


def authenticate():
    '''Authenticates the client library using default application
    credentials.'''
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('language', 'v1', credentials=credentials)
    return service


def getResponse(filename):
    '''Run sentiment analysis on text within a passed filename.'''
    service = authenticate()
    with open(filename, 'r') as review_file:
        service_request = service.documents().analyzeSentiment(
            body={
                'document': {
                    'type': 'PLAIN_TEXT',
                    'content': review_file.read(),
                }
            }
        )
        response = service_request.execute()
        return response


def printResponseContents(response):
    '''Prints document sentiment, magnitude, and sentence score.'''
    score = response['documentSentiment']['score']
    magnitude = response['documentSentiment']['magnitude']
    for i, sentence in enumerate(response['sentences']):
        sentence_sentiment = sentence['sentiment']['score']
        print('Sentence {} has a sentiment score of {}'.format(i,
              sentence_sentiment))
    print('Overall Sentiment: score of {} with magnitude of {}'.format(
            score, magnitude))


def main(filename):
    '''Run sentiment analysis on the file contents given a filename.'''
    printResponseContents(getResponse(filename))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'movie_review_filename',
        help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()
    main(args.movie_review_filename)
