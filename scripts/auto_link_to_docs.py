#!/usr/bin/env python

# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Process docs-links.json and updates all READMEs and replaces

<!-- auto-doc-link --><!-- end-auto-doc-link -->

With a generated list of documentation backlinks.
"""

from collections import defaultdict
import json
import os
import re


REPO_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..'))
DOC_SITE_ROOT = 'https://cloud.google.com'
AUTO_DOC_LINK_EXP = re.compile(
    r'<!-- auto-doc-link -->.*?<!-- end-auto-doc-link -->\n',
    re.DOTALL)


def invert_docs_link_map(docs_links):
    """
    The docs links map is in this format:

        {
            "doc_path": [
                "file_path",
            ]
        }

    This transforms it to:

        {
            "file_path": [
                "doc_path",
            ]
        }
    """
    files_to_docs = defaultdict(list)
    for doc, files in docs_links.iteritems():
        for file in files:
            files_to_docs[file].append(doc)
            files_to_docs[file] = list(set(files_to_docs[file]))

    return files_to_docs


def collect_docs_for_readmes(files_to_docs):
    """
    There's a one-to-many relationship between readmes and files. This method
    finds the readme for each file and consolidates all docs references.
    """
    readmes_to_docs = defaultdict(list)
    for file, docs in files_to_docs.iteritems():
        readme = get_readme_path(file)
        readmes_to_docs[readme].extend(docs)
        readmes_to_docs[readme] = list(set(readmes_to_docs[readme]))
    return readmes_to_docs


def linkify(docs):
    """Adds the documentation site root to doc paths, creating a full URL."""
    return [DOC_SITE_ROOT + x for x in docs]


def replace_contents(file_path, regex, new_content):
    with open(file_path, 'r+') as f:
        content = f.read()
        content = regex.sub(new_content, content)
        f.seek(0)
        f.write(content)


def get_readme_path(file_path):
    """Gets the readme for an associated sample file, basically just the
    README.md in the same directory."""
    dir = os.path.dirname(file_path)
    readme = os.path.join(
        REPO_ROOT, dir, 'README.md')
    return readme


def generate_doc_link_statement(docs):
    links = linkify(docs)
    if len(links) == 1:
        return """<!-- auto-doc-link -->
These samples are used on the following documentation page:

> {}

<!-- end-auto-doc-link -->
""".format(links.pop())
    else:
        return """<!-- auto-doc-link -->
These samples are used on the following documentation pages:

>
{}

<!-- end-auto-doc-link -->
""".format('\n'.join(['* {}'.format(x) for x in links]))


def update_readme(readme_path, docs):
    if not os.path.exists(readme_path):
        print('{} doesn\'t exist'.format(readme_path))
        return
    replace_contents(
        readme_path,
        AUTO_DOC_LINK_EXP,
        generate_doc_link_statement(docs))
    print('Updated {}'.format(readme_path))


def main():
    docs_links = json.load(open(
        os.path.join(
            REPO_ROOT, 'scripts', 'resources', 'docs-links.json'), 'r'))
    files_to_docs = invert_docs_link_map(docs_links)
    readmes_to_docs = collect_docs_for_readmes(files_to_docs)

    for readme, docs in readmes_to_docs.iteritems():
        update_readme(readme, docs)


if __name__ == '__main__':
    main()
