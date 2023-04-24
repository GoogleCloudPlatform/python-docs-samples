#!/usr/bin/env python

# Copyright 2017 Google LLC
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

"""Using the classify_text method to find content categories of text files,
Then use the content category labels to compare text similarity.

For more information, see the tutorial page at
https://cloud.google.com/natural-language/docs/classify-text-tutorial.
"""

# [START language_classify_text_tutorial_imports]
import argparse
import json
import os

from google.cloud import language_v1
import numpy

# [END language_classify_text_tutorial_imports]


# [START language_classify_text_tutorial_classify]
def classify(text, verbose=True):
    """Classify the input text into categories."""

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print("=" * 20)
            print("{:<16}: {}".format("category", category.name))
            print("{:<16}: {}".format("confidence", category.confidence))

    return result


# [END language_classify_text_tutorial_classify]


# [START language_classify_text_tutorial_index]
def index(path, index_file):
    """Classify each text file in a directory and write
    the results to the index_file.
    """

    result = {}
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        if not os.path.isfile(file_path):
            continue

        try:
            with open(file_path) as f:
                text = f.read()
                categories = classify(text, verbose=False)

                result[filename] = categories
        except Exception:
            print(f"Failed to process {file_path}")

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False))

    print(f"Texts indexed in file: {index_file}")
    return result


# [END language_classify_text_tutorial_index]


def split_labels(categories):
    """The category labels are of the form "/a/b/c" up to three levels,
    for example "/Computers & Electronics/Software", and these labels
    are used as keys in the categories dictionary, whose values are
    confidence scores.

    The split_labels function splits the keys into individual levels
    while duplicating the confidence score, which allows a natural
    boost in how we calculate similarity when more levels are in common.

    Example:
    If we have

    x = {"/a/b/c": 0.5}
    y = {"/a/b": 0.5}
    z = {"/a": 0.5}

    Then x and y are considered more similar than y and z.
    """
    _categories = {}
    for name, confidence in categories.items():
        labels = [label for label in name.split("/") if label]
        for label in labels:
            _categories[label] = confidence

    return _categories


def similarity(categories1, categories2):
    """Cosine similarity of the categories treated as sparse vectors."""
    categories1 = split_labels(categories1)
    categories2 = split_labels(categories2)

    norm1 = numpy.linalg.norm(list(categories1.values()))
    norm2 = numpy.linalg.norm(list(categories2.values()))

    # Return the smallest possible similarity if either categories is empty.
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # Compute the cosine similarity.
    dot = 0.0
    for label, confidence in categories1.items():
        dot += confidence * categories2.get(label, 0.0)

    return dot / (norm1 * norm2)


# [START language_classify_text_tutorial_query]
def query(index_file, text, n_top=3):
    """Find the indexed files that are the most similar to
    the query text.
    """

    with open(index_file) as f:
        index = json.load(f)

    # Get the categories of the query text.
    query_categories = classify(text, verbose=False)

    similarities = []
    for filename, categories in index.items():
        similarities.append((filename, similarity(query_categories, categories)))

    similarities = sorted(similarities, key=lambda p: p[1], reverse=True)

    print("=" * 20)
    print(f"Query: {text}\n")
    for category, confidence in query_categories.items():
        print(f"\tCategory: {category}, confidence: {confidence}")
    print(f"\nMost similar {n_top} indexed texts:")
    for filename, sim in similarities[:n_top]:
        print(f"\tFilename: {filename}")
        print(f"\tSimilarity: {sim}")
        print("\n")

    return similarities


# [END language_classify_text_tutorial_query]


# [START language_classify_text_tutorial_query_category]
def query_category(index_file, category_string, n_top=3):
    """Find the indexed files that are the most similar to
    the query label.

    The list of all available labels:
    https://cloud.google.com/natural-language/docs/categories
    """

    with open(index_file) as f:
        index = json.load(f)

    # Make the category_string into a dictionary so that it is
    # of the same format as what we get by calling classify.
    query_categories = {category_string: 1.0}

    similarities = []
    for filename, categories in index.items():
        similarities.append((filename, similarity(query_categories, categories)))

    similarities = sorted(similarities, key=lambda p: p[1], reverse=True)

    print("=" * 20)
    print(f"Query: {category_string}\n")
    print(f"\nMost similar {n_top} indexed texts:")
    for filename, sim in similarities[:n_top]:
        print(f"\tFilename: {filename}")
        print(f"\tSimilarity: {sim}")
        print("\n")

    return similarities


# [END language_classify_text_tutorial_query_category]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")
    classify_parser = subparsers.add_parser("classify", help=classify.__doc__)
    classify_parser.add_argument(
        "text",
        help="The text to be classified. " "The text needs to have at least 20 tokens.",
    )
    index_parser = subparsers.add_parser("index", help=index.__doc__)
    index_parser.add_argument(
        "path", help="The directory that contains " "text files to be indexed."
    )
    index_parser.add_argument(
        "--index_file", help="Filename for the output JSON.", default="index.json"
    )
    query_parser = subparsers.add_parser("query", help=query.__doc__)
    query_parser.add_argument("index_file", help="Path to the index JSON file.")
    query_parser.add_argument("text", help="Query text.")
    query_category_parser = subparsers.add_parser(
        "query-category", help=query_category.__doc__
    )
    query_category_parser.add_argument(
        "index_file", help="Path to the index JSON file."
    )
    query_category_parser.add_argument("category", help="Query category.")

    args = parser.parse_args()

    if args.command == "classify":
        classify(args.text)
    if args.command == "index":
        index(args.path, args.index_file)
    if args.command == "query":
        query(args.index_file, args.text)
    if args.command == "query-category":
        query_category(args.index_file, args.category)
