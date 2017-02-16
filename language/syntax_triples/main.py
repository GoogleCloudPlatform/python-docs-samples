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
This example finds subject-verb-object triples in a given piece of text using
the syntax analysis capabilities of Cloud Natural Language API. The triples are
printed to STDOUT. This can be considered as the first step towards an
information extraction task.

Run the script on a file containing the text that you wish to analyze.
The text must be encoded in UTF8 or ASCII:
    $ python main.py <path-to-text-file>

Try this on a sample text in the resources directory:
    $ python main.py resources/obama_wikipedia.txt
"""

import argparse
import sys
import textwrap

import googleapiclient.discovery


def dependents(tokens, head_index):
    """Returns an ordered list of the token indices of the dependents for
    the given head."""
    # Create head->dependency index.
    head_to_deps = {}
    for i, token in enumerate(tokens):
        head = token['dependencyEdge']['headTokenIndex']
        if i != head:
            head_to_deps.setdefault(head, []).append(i)
    return head_to_deps.get(head_index, ())


def phrase_text_for_head(tokens, text, head_index):
    """Returns the entire phrase containing the head token
    and its dependents.
    """
    begin, end = phrase_extent_for_head(tokens, head_index)
    return text[begin:end]


def phrase_extent_for_head(tokens, head_index):
    """Returns the begin and end offsets for the entire phrase
    containing the head token and its dependents.
    """
    begin = tokens[head_index]['text']['beginOffset']
    end = begin + len(tokens[head_index]['text']['content'])
    for child in dependents(tokens, head_index):
        child_begin, child_end = phrase_extent_for_head(tokens, child)
        begin = min(begin, child_begin)
        end = max(end, child_end)
    return (begin, end)


def analyze_syntax(text):
    """Use the NL API to analyze the given text string, and returns the
    response from the API.  Requests an encodingType that matches
    the encoding used natively by Python.  Raises an
    errors.HTTPError if there is a connection problem.
    """
    service = googleapiclient.discovery.build('language', 'v1beta1')
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extract_syntax': True,
        },
        'encodingType': get_native_encoding_type(),
    }
    request = service.documents().annotateText(body=body)
    return request.execute()


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def find_triples(tokens,
                 left_dependency_label='NSUBJ',
                 head_part_of_speech='VERB',
                 right_dependency_label='DOBJ'):
    """Generator function that searches the given tokens
    with the given part of speech tag, that have dependencies
    with the given labels.  For each such head found, yields a tuple
    (left_dependent, head, right_dependent), where each element of the
    tuple is an index into the tokens array.
    """
    for head, token in enumerate(tokens):
        if token['partOfSpeech']['tag'] == head_part_of_speech:
            children = dependents(tokens, head)
            left_deps = []
            right_deps = []
            for child in children:
                child_token = tokens[child]
                child_dep_label = child_token['dependencyEdge']['label']
                if child_dep_label == left_dependency_label:
                    left_deps.append(child)
                elif child_dep_label == right_dependency_label:
                    right_deps.append(child)
            for left_dep in left_deps:
                for right_dep in right_deps:
                    yield (left_dep, head, right_dep)


def show_triple(tokens, text, triple):
    """Prints the given triple (left, head, right).  For left and right,
    the entire phrase headed by each token is shown.  For head, only
    the head token itself is shown.

    """
    nsubj, verb, dobj = triple

    # Extract the text for each element of the triple.
    nsubj_text = phrase_text_for_head(tokens, text, nsubj)
    verb_text = tokens[verb]['text']['content']
    dobj_text = phrase_text_for_head(tokens, text, dobj)

    # Pretty-print the triple.
    left = textwrap.wrap(nsubj_text, width=28)
    mid = textwrap.wrap(verb_text, width=10)
    right = textwrap.wrap(dobj_text, width=28)
    print('+' + 30 * '-' + '+' + 12 * '-' + '+' + 30 * '-' + '+')
    for l, m, r in zip(left, mid, right):
        print('| {:<28s} | {:<10s} | {:<28s} |'.format(
            l or '', m or '', r or ''))


def main(text_file):
    # Extracts subject-verb-object triples from the given text file,
    # and print each one.

    # Read the input file.
    text = open(text_file, 'rb').read().decode('utf8')

    analysis = analyze_syntax(text)
    tokens = analysis.get('tokens', [])

    for triple in find_triples(tokens):
        show_triple(tokens, text, triple)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'text_file',
        help='A file containing the document to process.  '
        'Should be encoded in UTF8 or ASCII')
    args = parser.parse_args()
    main(args.text_file)
