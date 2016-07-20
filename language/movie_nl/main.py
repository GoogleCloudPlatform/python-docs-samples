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

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import requests


def analyze_document(service, document):
    """Analyze the document and get the distribution of sentiments and
    the movie name."""
    logging.info('Analyzing {}'.format(document.doc_id))

    sentences, entities = document.extract_all_sentences(service)
    sentiments = [get_sentiment(service, sentence) for sentence in sentences]

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


def get_sentiment(service, sentence):
    """Get the sentence-level sentiment."""
    body = get_request_body(
        sentence, syntax=False, entities=True, sentiment=True)

    docs = service.documents()
    request = docs.annotateText(body=body)
    response = request.execute()
    sentiment = response.get("documentSentiment")

    if sentiment is None:
        return (None, None)
    else:
        pol = sentiment.get("polarity")
        mag = sentiment.get("magnitude")

    if pol is None and mag is not None:
        pol = 0
    return (pol, mag)


class Document(object):
    """Document class captures a single document of movie reviews."""

    def __init__(self, text, doc_id, doc_path):
        self.text = text
        self.doc_id = doc_id
        self.doc_path = doc_path
        self.sentent_pair = None
        self.label = None

    def extract_all_sentences(self, service):
        """Extract the sentences in a document."""

        if self.sentent_pair is None:
            docs = service.documents()
            request_body = get_request_body(
                self.text,
                syntax=True,
                entities=True,
                sentiment=False)
            request = docs.annotateText(body=request_body)

            ent_list = []

            response = request.execute()
            entities = response.get('entities', [])
            sentences = response.get('sentences', [])

            sent_list = [
                sentence.get('text').get('content') for sentence in sentences
            ]

            for entity in entities:
                ent_type = entity.get('type')
                wiki_url = entity.get('metadata', {}).get('wikipedia_url')

                if ent_type == 'PERSON' and wiki_url is not None:
                    ent_list.append(wiki_url)

            self.sentent_pair = (sent_list, ent_list)

        return self.sentent_pair


def to_sentiment_json(doc_id, sent, label):
    """Convert the sentiment info to json."""
    json_doc = {}

    json_doc['doc_id'] = doc_id
    json_doc['sentiment'] = float('%.3f' % sent)
    json_doc['label'] = label

    return json.dumps(json_doc)


def get_wiki_title(wiki_url):
    """Get the wikipedia page title for a given wikipedia URL."""
    try:
        content = requests.get(wiki_url).text
        return content.split('title')[1].split('-')[0].split('>')[1].strip()
    except:
        return os.path.basename(wiki_url).replace('_', ' ')


def to_entity_json(entity, e_tuple):
    """Convert the entity info to json."""
    json_doc = {}

    avg_sentiment = float(e_tuple[0]) / float(e_tuple[1])

    json_doc['wiki_url'] = entity
    json_doc['name'] = get_wiki_title(entity)
    json_doc['sentiment'] = float('%.3f' % e_tuple[0])
    json_doc['avg_sentiment'] = float('%.3f' % avg_sentiment)

    return json.dumps(json_doc)


def get_sentiment_entities(service, document):
    """Compute the overall sentiment volume in the document"""
    sentiments, entities = analyze_document(service, document)

    sentiments = [sent for sent in sentiments if sent[0] is not None]
    negative_sentiments = [
        polarity for polarity, magnitude in sentiments if polarity < 0.0]
    positive_sentiments = [
        polarity for polarity, magnitude in sentiments if polarity > 0.0]

    negative = sum(negative_sentiments)
    positive = sum(positive_sentiments)
    total = positive + negative

    return (total, entities)


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
        sentiment_total, entities = get_sentiment_entities(
            service, document)
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

    for entity, e_tuple in collected_entities.items():
        entity_writer.write(to_entity_json(entity, e_tuple))
        entity_writer.write('\n')

    sentiment_writer.flush()
    entity_writer.flush()


def document_generator(dir_path_pattern, count=None):
    """Generator for the input movie documents."""
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

    items.sort(reverse=True)
    items = [json.dumps(item[1]) for item in items]

    if reverse_bool:
        items.reverse()

    if topn:
        print('\n'.join(items[:topn]))
    else:
        print('\n'.join(items))


def get_service():
    """Build a client to the Google Cloud Natural Language API."""

    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    return discovery.build('language', 'v1beta1', http=http)


def analyze(input_dir, sentiment_writer, entity_writer, sample, log_file):
    """Movie demo main program"""

    # Create logger settings
    logging.basicConfig(filename=log_file, level=logging.DEBUG)

    # Create a Google Service object
    service = get_service()

    reader = document_generator(input_dir, sample)

    # Process the movie documents
    process_movie_reviews(service, reader, sentiment_writer, entity_writer)

    # close reader and writers
    sentiment_writer.close()
    entity_writer.close()
    reader.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    rank_parser = subparsers.add_parser('rank')

    rank_parser.add_argument(
        'entity_input', help='location of entity input',
        type=argparse.FileType('r'))
    rank_parser.add_argument(
        '--sentiment', help='filter sentiment as "neg" or "pos"')
    rank_parser.add_argument(
        '--reverse', help='reverse the order of the items')
    rank_parser.add_argument(
        '--sample', help='number of top items to process', type=int)

    analyze_parser = subparsers.add_parser('analyze')

    analyze_parser.add_argument(
        '--inp', help='location of the input', required=True)
    analyze_parser.add_argument(
        '--sout', help='location of the sentiment output', required=True,
        type=argparse.FileType('w'))
    analyze_parser.add_argument(
        '--eout', help='location of the entity output', required=True,
        type=argparse.FileType('w'))
    analyze_parser.add_argument(
        '--sample', help='number of top items to process', type=int)
    analyze_parser.add_argument('--log_file', default='movie.log')

    args = parser.parse_args()

    if args.command == 'analyze':
        analyze(args.inp, args.sout, args.eout, args.sample, args.log_file)
    elif args.command == 'rank':
        rank_entities(
            args.entity_input, args.sentiment, args.sample, args.reverse)
