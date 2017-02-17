#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This example uses the Google Cloud Vision API to detect text in images, then
analyzes that text using the Google Cloud Natural Language API to detect
entities in the text. It stores the detected entity information in an sqlite3
database, which may then be queried.

After this script has analyzed a directory of images, it outputs some
information on the images' entities to STDOUT. You can also further query
the generated sqlite3 database; see the README for more information.

Run the script on a directory of images to do the analysis, E.g.:
    $ python main.py --input_directory=<path-to-image-directory>

You can try this on a sample directory of images:
    $ curl -O http://storage.googleapis.com/python-docs-samples-tests/language/ocr_nl-images.zip
    $ unzip ocr_nl-images.zip
    $ python main.py --input_directory=images/

"""  # noqa

import argparse
import base64
import contextlib
import logging
import os
import sqlite3
import sys
import time

import googleapiclient.discovery
import googleapiclient.errors

BATCH_SIZE = 10


class VisionApi(object):
    """Construct and use the Cloud Vision API service."""

    def __init__(self):
        self.service = googleapiclient.discovery.build('vision', 'v1')

    def detect_text(self, input_filenames, num_retries=3, max_results=6):
        """Uses the Vision API to detect text in the given file."""
        batch_request = []
        for filename in input_filenames:
            request = {
                'image': {},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': max_results,
                }]
            }

            # Accept both files in cloud storage, as well as local files.
            if filename.startswith('gs://'):
                request['image']['source'] = {
                    'gcsImageUri': filename
                }
            else:
                with open(filename, 'rb') as image_file:
                    request['image']['content'] = base64.b64encode(
                        image_file.read()).decode('UTF-8')

            batch_request.append(request)

        request = self.service.images().annotate(
            body={'requests': batch_request})

        try:
            responses = request.execute(num_retries=num_retries)
            if 'responses' not in responses:
                return {}

            text_response = {}
            for filename, response in zip(
                    input_filenames, responses['responses']):

                if 'error' in response:
                    logging.error('API Error for {}: {}'.format(
                        filename,
                        response['error'].get('message', '')))
                    continue

                text_response[filename] = response.get('textAnnotations', [])

            return text_response

        except googleapiclient.errors.HttpError as e:
            logging.error('Http Error for {}: {}'.format(filename, e))
        except KeyError as e2:
            logging.error('Key error: {}'.format(e2))


class TextAnalyzer(object):
    """Construct and use the Google Natural Language API service."""

    def __init__(self, db_filename=None):
        self.service = googleapiclient.discovery.build('language', 'v1')

        # This list will store the entity information gleaned from the
        # image files.
        self.entity_info = []

        # This is the filename of the sqlite3 database to save to
        self.db_filename = db_filename or 'entities{}.db'.format(
            int(time.time()))

    def _get_native_encoding_type(self):
        """Returns the encoding type that matches Python's native strings."""
        if sys.maxunicode == 65535:
            return 'UTF16'
        else:
            return 'UTF32'

    def nl_detect(self, text):
        """Use the Natural Language API to analyze the given text string."""
        # We're only requesting 'entity' information from the Natural Language
        # API at this time.
        body = {
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text,
            },
            'encodingType': self._get_native_encoding_type(),
        }
        entities = []
        try:
            request = self.service.documents().analyzeEntities(body=body)
            response = request.execute()
            entities = response['entities']
        except googleapiclient.errors.HttpError as e:
            logging.error('Http Error: %s' % e)
        except KeyError as e2:
            logging.error('Key error: %s' % e2)
        return entities

    def add_entities(self, filename, locale, document):
        """Apply the Natural Language API to the document, and collect the
        detected entities."""

        # Apply the Natural Language API to the document.
        entities = self.nl_detect(document)
        self.extract_and_save_entity_info(entities, locale, filename)

    def extract_entity_info(self, entity):
        """Extract information about an entity."""
        type = entity['type']
        name = entity['name'].lower()
        metadata = entity['metadata']
        salience = entity['salience']
        wiki_url = metadata.get('wikipedia_url', None)
        return (type, name, salience, wiki_url)

    def extract_and_save_entity_info(self, entities, locale, filename):
        for entity in entities:
            type, name, salience, wiki_url = self.extract_entity_info(entity)
            # Because this is a small example, we're using a list to hold
            # all the entity information, then we'll insert it into the
            # database all at once when we've processed all the files.
            # For a larger data set, you would want to write to the database
            # in batches.
            self.entity_info.append(
                (locale, type, name, salience, wiki_url, filename))

    def write_entity_info_to_db(self):
        """Store the info gleaned about the entities in the text, via the
        Natural Language API, in an sqlite3 database table, and then print out
        some simple analytics.
        """
        logging.info('Saving entity info to the sqlite3 database.')
        # Create the db.
        with contextlib.closing(sqlite3.connect(self.db_filename)) as conn:
            with conn as cursor:
                # Create table
                cursor.execute(
                    'CREATE TABLE if not exists entities (locale text, '
                    'type text, name text, salience real, wiki_url text, '
                    'filename text)')
            with conn as cursor:
                # Load all the data
                cursor.executemany(
                    'INSERT INTO entities VALUES (?,?,?,?,?,?)',
                    self.entity_info)

    def output_entity_data(self):
        """Output some info about the entities by querying the generated
        sqlite3 database.
        """

        with contextlib.closing(sqlite3.connect(self.db_filename)) as conn:

            # This query finds the number of times each entity name was
            # detected, in descending order by count, and returns information
            # about the first 15 names, including the files in which they were
            # found, their detected 'salience' and language (locale), and the
            # wikipedia urls (if any) associated with them.
            print('\n==============\nTop 15 most frequent entity names:')

            cursor = conn.cursor()
            results = cursor.execute(
                'select name, count(name) as wc from entities '
                'group by name order by wc desc limit 15;')

            for item in results:
                cursor2 = conn.cursor()
                print(u'\n----Name: {} was found with count {}'.format(*item))
                results2 = cursor2.execute(
                    'SELECT name, type, filename, locale, wiki_url, salience '
                    'FROM entities WHERE name=?', (item[0],))
                urls = set()
                for elt in results2:
                    print(('Found in file {}, detected as type {}, with\n'
                           '  locale {} and salience {}.').format(
                               elt[2], elt[1], elt[3], elt[5]))
                    if elt[4]:
                        urls.add(elt[4])
                if urls:
                    print('url(s): {}'.format(urls))

            # This query finds the number of times each wikipedia url was
            # detected, in descending order by count, and returns information
            # about the first 15 urls, including the files in which they were
            # found and the names and 'salience' with which they were
            # associated.
            print('\n==============\nTop 15 most frequent Wikipedia URLs:')
            c = conn.cursor()
            results = c.execute(
                'select wiki_url, count(wiki_url) as wc from entities '
                'group by wiki_url order by wc desc limit 15;')

            for item in results:
                cursor2 = conn.cursor()
                print('\n----entity: {} was found with count {}'.format(*item))
                results2 = cursor2.execute(
                    'SELECT name, type, filename, locale, salience '
                    'FROM entities WHERE wiki_url=?', (item[0],))
                names = set()
                salience = set()
                for elt in results2:
                    print(('Found in file {}, detected as type {}, with\n'
                           '  locale {}.').format(elt[2], elt[1], elt[3]))
                    names.add(elt[0])
                    salience.add(elt[4])
                print('names(s): {}'.format(names))
                print('salience measure(s): {}'.format(salience))


def extract_description(texts):
    """Returns text annotations as a single string"""
    document = []

    for text in texts:
        try:
            document.append(text['description'])
            locale = text['locale']
            # Process only the first entry, which contains all
            # text detected.
            break
        except KeyError as e:
            logging.error('KeyError: %s\n%s' % (e, text))
    return (locale, ' '.join(document))


def extract_descriptions(input_filename, texts, text_analyzer):
    """Gets the text that was detected in the image."""
    if texts:
        locale, document = extract_description(texts)
        text_analyzer.add_entities(input_filename, locale, document)
        sys.stdout.write('.')  # Output a progress indicator.
        sys.stdout.flush()
    elif texts == []:
        print('%s had no discernible text.' % input_filename)


def get_text_from_files(vision, input_filenames, text_analyzer):
    """Call the Vision API on a file and index the results."""
    texts = vision.detect_text(input_filenames)
    if texts:
        for filename, text in texts.items():
            extract_descriptions(filename, text, text_analyzer)


def batch(list_to_batch, batch_size=BATCH_SIZE):
    """Group a list into batches of size batch_size.

    >>> tuple(batch([1, 2, 3, 4, 5], batch_size=2))
    ((1, 2), (3, 4), (5))
    """
    for i in range(0, len(list_to_batch), batch_size):
        yield tuple(list_to_batch[i:i + batch_size])


def main(input_dir, db_filename=None):
    """Walk through all the image files in the given directory, extracting any
    text from them and feeding that text to the Natural Language API for
    analysis.
    """
    # Create a client object for the Vision API
    vision_api_client = VisionApi()
    # Create an object to analyze our text using the Natural Language API
    text_analyzer = TextAnalyzer(db_filename)

    if input_dir:
        allfileslist = []
        # Recursively construct a list of all the files in the given input
        # directory.
        for folder, subs, files in os.walk(input_dir):
            for filename in files:
                allfileslist.append(os.path.join(folder, filename))

        # Analyze the text in the files using the Vision and Natural Language
        # APIs.
        for filenames in batch(allfileslist, batch_size=1):
            get_text_from_files(vision_api_client, filenames, text_analyzer)

        # Save the result to a database, then run some queries on the database,
        # with output to STDOUT.
        text_analyzer.write_entity_info_to_db()

    # now, print some information about the entities detected.
    text_analyzer.output_entity_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects text in the images in the given directory.')
    parser.add_argument(
        '--input_directory',
        help='The image directory you\'d like to detect text in. If left '
        'unspecified, the --db specified will be queried without being '
        'updated.')
    parser.add_argument(
        '--db', help='The filename to use for the sqlite3 database.')
    args = parser.parse_args()

    if not (args.input_directory or args.db):
        parser.error('Either --input_directory or --db must be specified.')

    main(args.input_directory, args.db)
