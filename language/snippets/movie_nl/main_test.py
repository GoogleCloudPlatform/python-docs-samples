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

import json

import googleapiclient.discovery
import six

import main


def test_get_request_body():
    text = 'hello world'
    body = main.get_request_body(text, syntax=True, entities=True,
                                 sentiment=False)
    assert body.get('document').get('content') == text

    assert body.get('features').get('extract_syntax') is True
    assert body.get('features').get('extract_entities') is True
    assert body.get('features').get('extract_document_sentiment') is False


def test_get_sentiment_label():
    assert main.get_sentiment_label(20.50) == 1
    assert main.get_sentiment_label(-42.34) == -1


def test_to_sentiment_json():
    doc_id = '12345'
    sentiment = 23.344564
    label = 1

    sentiment_json = json.loads(
        main.to_sentiment_json(doc_id, sentiment, label)
    )

    assert sentiment_json.get('doc_id') == doc_id
    assert sentiment_json.get('sentiment') == 23.345
    assert sentiment_json.get('label') == label


def test_process_movie_reviews():
    service = googleapiclient.discovery.build('language', 'v1')

    doc1 = main.Document('Top Gun was awesome and Tom Cruise rocked!', 'doc1',
                         'doc1')
    doc2 = main.Document('Tom Cruise is a great actor.', 'doc2', 'doc2')

    reader = [doc1, doc2]
    swriter = six.StringIO()
    ewriter = six.StringIO()

    main.process_movie_reviews(service, reader, swriter, ewriter)

    sentiments = swriter.getvalue().strip().split('\n')
    entities = ewriter.getvalue().strip().split('\n')

    sentiments = [json.loads(sentiment) for sentiment in sentiments]
    entities = [json.loads(entity) for entity in entities]

    # assert sentiments
    assert sentiments[0].get('sentiment') > 0
    assert sentiments[0].get('label') == 1

    assert sentiments[1].get('sentiment') > 0
    assert sentiments[1].get('label') == 1

    # assert entities
    assert len(entities) == 1
    assert entities[0].get('name') == 'Tom Cruise'
    assert (entities[0].get('wiki_url') ==
            'https://en.wikipedia.org/wiki/Tom_Cruise')
    assert entities[0].get('sentiment') > 0


def test_rank_positive_entities(capsys):
    reader = [
        ('{"avg_sentiment": -12.0, '
         '"name": "Patrick Macnee", "sentiment": -12.0}'),
        ('{"avg_sentiment": 5.0, '
         '"name": "Paul Rudd", "sentiment": 5.0}'),
        ('{"avg_sentiment": -5.0, '
         '"name": "Martha Plimpton", "sentiment": -5.0}'),
        ('{"avg_sentiment": 7.0, '
         '"name": "Lucy (2014 film)", "sentiment": 7.0}')
    ]

    main.rank_entities(reader, 'pos', topn=1, reverse_bool=False)
    out, err = capsys.readouterr()

    expected = ('{"avg_sentiment": 5.0, '
                '"name": "Paul Rudd", "sentiment": 5.0}')

    expected = ''.join(sorted(expected))
    out = ''.join(sorted(out.strip()))
    assert out == expected


def test_rank_negative_entities(capsys):
    reader = [
        ('{"avg_sentiment": -12.0, '
         '"name": "Patrick Macnee", "sentiment": -12.0}'),
        ('{"avg_sentiment": 5.0, '
         '"name": "Paul Rudd", "sentiment": 5.0}'),
        ('{"avg_sentiment": -5.0, '
         '"name": "Martha Plimpton", "sentiment": -5.0}'),
        ('{"avg_sentiment": 7.0, '
         '"name": "Lucy (2014 film)", "sentiment": 7.0}')
    ]

    main.rank_entities(reader, 'neg', topn=1, reverse_bool=True)
    out, err = capsys.readouterr()

    expected = ('{"avg_sentiment": -5.0, '
                '"name": "Martha Plimpton", "sentiment": -5.0}')

    expected = ''.join(sorted(expected))
    out = ''.join(sorted(out.strip()))
    assert out == expected
