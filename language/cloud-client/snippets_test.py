# Copyright 2016 Google, Inc.
#
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


import snippets


def test_sentiment_text(cloud_config, capsys):
    snippets.sentiment_text('President Obama is speaking at the White House.')
    out, _ = capsys.readouterr()
    assert 'Score: 0.2' in out


def test_sentiment_file(cloud_config, capsys):
    cloud_storage_input_uri = 'gs://{}/text.txt'.format(
        cloud_config.storage_bucket)
    snippets.sentiment_file(cloud_storage_input_uri)
    out, _ = capsys.readouterr()
    assert 'Score: 0.2' in out


def test_entities_text(cloud_config, capsys):
    snippets.entities_text('President Obama is speaking at the White House.')
    out, _ = capsys.readouterr()
    assert 'name' in out
    assert ': Obama' in out


def test_entities_file(cloud_config, capsys):
    cloud_storage_input_uri = 'gs://{}/text.txt'.format(
        cloud_config.storage_bucket)
    snippets.entities_file(cloud_storage_input_uri)
    out, _ = capsys.readouterr()
    assert 'name' in out
    assert ': Obama' in out


def test_syntax_text(cloud_config, capsys):
    snippets.syntax_text('President Obama is speaking at the White House.')
    out, _ = capsys.readouterr()
    assert 'NOUN: President' in out


def test_syntax_file(cloud_config, capsys):
    cloud_storage_input_uri = 'gs://{}/text.txt'.format(
        cloud_config.storage_bucket)
    snippets.syntax_file(cloud_storage_input_uri)
    out, _ = capsys.readouterr()
    assert 'NOUN: President' in out
