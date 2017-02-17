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
import codecs
import glob
import json
import logging
import os

import googleapiclient.discovery
from googleapiclient.errors import HttpError
import requests


def analyze_document(service, document):
    """Analyze the document and get the distribution of sentiments and
    the movie name."""
    logging.info('Analyzing {}'.format(document.doc_id))

    sentiments, entities = document.extract_sentiment_entities(service)
    return sentiments, entities


def get_request_body(text, syntax=True, entities=True, sentiment=True):
    """Creates the body of the request to the language api in
    order to get an appropriate api response."""
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extract_syntax': syntax,
            'extract_entities': entities,
            'extract_document_sentiment': sentiment,
        },
        'encoding_type': 'UTF32'
    }

    return body


class Document(object):
    """Document class captures a single document of movie reviews."""

    def __init__(self, text, doc_id, doc_path):
        self.text = text
        self.doc_id = doc_id
        self.doc_path = doc_path
        self.sentiment_entity_pair = None
        self.label = None

    def extract_sentiment_entities(self, service):
        """Extract the sentences in a document."""

        if self.sentiment_entity_pair is not None:
            return self.sentence_entity_pair

        docs = service.documents()
        request_body = get_request_body(
            self.text,
            syntax=False,
            entities=True,
            sentiment=True)
        request = docs.annotateText(body=request_body)

        ent_list = []

        response = request.execute()
        entities = response.get('entities', [])
        documentSentiment = response.get('documentSentiment', {})

        for entity in entities:
            ent_type = entity.get('type')
            wiki_url = entity.get('metadata', {}).get('wikipedia_url')

            if ent_type == 'PERSON' and wiki_url is not None:
                ent_list.append(wiki_url)

        self.sentiment_entity_pair = (documentSentiment, ent_list)

        return self.sentiment_entity_pair


def to_sentiment_json(doc_id, sent, label):
    """Convert the sentiment info to json.

    Args:
        doc_id: Document id
        sent: Overall Sentiment for the document
        label: Actual label +1, 0, -1 for the document

    Returns:
        String json representation of the input

    """
    json_doc = {}

    json_doc['doc_id'] = doc_id
    json_doc['sentiment'] = float('%.3f' % sent)
    json_doc['label'] = label

    return json.dumps(json_doc)


def get_wiki_title(wiki_url):
    """Get the wikipedia page title for a given wikipedia URL.

    Args:
        wiki_url: Wikipedia URL e.g., http://en.wikipedia.org/wiki/Sean_Connery

    Returns:
        Wikipedia canonical name e.g., Sean Connery

    """
    try:
        content = requests.get(wiki_url).text
        return content.split('title')[1].split('-')[0].split('>')[1].strip()
    except:
        return os.path.basename(wiki_url).replace('_', ' ')


def to_entity_json(entity, entity_sentiment, entity_frequency):
    """Convert entities and their associated sentiment to json.

    Args:
        entity: Wikipedia entity name
        entity_sentiment: Sentiment associated with the entity
        entity_frequency: Frequency of the entity in the corpus

    Returns:
       Json string representation of input

    """
    json_doc = {}

    avg_sentiment = float(entity_sentiment) / float(entity_frequency)

    json_doc['wiki_url'] = entity
    json_doc['name'] = get_wiki_title(entity)
    json_doc['sentiment'] = float('%.3f' % entity_sentiment)
    json_doc['avg_sentiment'] = float('%.3f' % avg_sentiment)

    return json.dumps(json_doc)


def get_sentiment_entities(service, document):
    """Compute the overall sentiment volume in the document.

    Args:
        service: Client to Google Natural Language API
        document: Movie review document (See Document object)

    Returns:
        Tuple of total sentiment and entities found in the document

    """

    sentiments, entities = analyze_document(service, document)
    score = sentiments.get('score')

    return (score, entities)


def get_sentiment_label(sentiment):
    """Return the sentiment label based on the sentiment quantity."""
    if sentiment < 0:
        return -1
    elif sentiment > 0:
        return 1
    else:
        return 0


def process_movie_reviews(service, reader, sentiment_writer, entity_writer):
    """Perform some sentiment math and come up with movie review."""
    collected_entities = {}

    for document in reader:
        try:
            sentiment_total, entities = get_sentiment_entities(
                service, document)
        except HttpError as e:
            logging.error('Error process_movie_reviews {}'.format(e.content))
            continue

        document.label = get_sentiment_label(sentiment_total)

        sentiment_writer.write(
            to_sentiment_json(
                document.doc_id,
                sentiment_total,
                document.label
            )
        )

        sentiment_writer.write('\n')

        for ent in entities:
            ent_sent, frequency = collected_entities.get(ent, (0, 0))
            ent_sent += sentiment_total
            frequency += 1

            collected_entities[ent] = (ent_sent, frequency)

    for entity, sentiment_frequency in collected_entities.items():
        entity_writer.write(to_entity_json(entity, sentiment_frequency[0],
                                           sentiment_frequency[1]))
        entity_writer.write('\n')

    sentiment_writer.flush()
    entity_writer.flush()


def document_generator(dir_path_pattern, count=None):
    """Generator for the input movie documents.

    Args:
        dir_path_pattern: Input dir pattern e.g., "foo/bar/*/*"
        count: Number of documents to read else everything if None

    Returns:
        Generator which contains Document (See above)

    """
    for running_count, item in enumerate(glob.iglob(dir_path_pattern)):
        if count and running_count >= count:
            raise StopIteration()

        doc_id = os.path.basename(item)

        with codecs.open(item, encoding='utf-8') as f:
            try:
                text = f.read()
            except UnicodeDecodeError:
                continue

            yield Document(text, doc_id, item)


def rank_entities(reader, sentiment=None, topn=None, reverse_bool=False):
    """Rank the entities (actors) based on their sentiment
    assigned from the movie."""

    items = []
    for item in reader:
        json_item = json.loads(item)
        sent = json_item.get('sentiment')
        entity_item = (sent, json_item)

        if sentiment:
            if sentiment == 'pos' and sent > 0:
                items.append(entity_item)
            elif sentiment == 'neg' and sent < 0:
                items.append(entity_item)
        else:
            items.append(entity_item)

    items.sort(reverse=reverse_bool)
    items = [json.dumps(item[1]) for item in items]

    print('\n'.join(items[:topn]))


def analyze(input_dir, sentiment_writer, entity_writer, sample, log_file):
    """Analyze the document for sentiment and entities"""

    # Create logger settings
    logging.basicConfig(filename=log_file, level=logging.DEBUG)

    # Create a Google Service object
    service = googleapiclient.discovery.build('language', 'v1')

    reader = document_generator(input_dir, sample)

    # Process the movie documents
    process_movie_reviews(service, reader, sentiment_writer, entity_writer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    rank_parser = subparsers.add_parser('rank')

    rank_parser.add_argument(
        '--entity_input', help='location of entity input')
    rank_parser.add_argument(
        '--sentiment', help='filter sentiment as "neg" or "pos"')
    rank_parser.add_argument(
        '--reverse', help='reverse the order of the items', type=bool,
        default=False
        )
    rank_parser.add_argument(
        '--sample', help='number of top items to process', type=int,
        default=None
        )

    analyze_parser = subparsers.add_parser('analyze')

    analyze_parser.add_argument(
        '--inp', help='location of the input', required=True)
    analyze_parser.add_argument(
        '--sout', help='location of the sentiment output', required=True)
    analyze_parser.add_argument(
        '--eout', help='location of the entity output', required=True)
    analyze_parser.add_argument(
        '--sample', help='number of top items to process', type=int)
    analyze_parser.add_argument('--log_file', default='movie.log')

    args = parser.parse_args()

    if args.command == 'analyze':
        with open(args.sout, 'w') as sout, open(args.eout, 'w') as eout:
            analyze(args.inp, sout, eout, args.sample, args.log_file)
    elif args.command == 'rank':
        with open(args.entity_input, 'r') as entity_input:
            rank_entities(
                entity_input, args.sentiment, args.sample, args.reverse)
