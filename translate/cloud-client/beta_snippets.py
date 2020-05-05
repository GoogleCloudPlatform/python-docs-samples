# -*- coding: utf-8 -*-
# Copyright 2019 Google LLC
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

import argparse


def translate_text(project_id, text):
    # [START translate_translate_text_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = YOUR_PROJECT_ID
    # text = 'Text you wish to translate'
    location = 'global'

    parent = client.location_path(project_id, location)

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='en-US',
        target_language_code='sr-Latn')

    for translation in response.translations:
        print(u'Translated Text: {}'.format(translation))
    # [END translate_translate_text_beta]


def batch_translate_text(project_id, input_uri, output_uri):
    # [START translate_batch_translate_text_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = YOUR_PROJECT_ID
    # input_uri = 'gs://cloud-samples-data/translation/text.txt'
    # output_uri = 'gs://YOUR_BUCKET_ID/path_to_store_results/'
    location = 'us-central1'

    parent = client.location_path(project_id, location)

    gcs_source = translate.types.GcsSource(input_uri=input_uri)

    input_config = translate.types.InputConfig(
        mime_type='text/plain',  # mime types: text/plain, text/html
        gcs_source=gcs_source)

    gcs_destination = translate.types.GcsDestination(
        output_uri_prefix=output_uri)

    output_config = translate.types.OutputConfig(
        gcs_destination=gcs_destination)

    operation = client.batch_translate_text(
        parent=parent,
        source_language_code='en-US',
        target_language_codes=['sr-Latn'],
        input_configs=[input_config],
        output_config=output_config)

    result = operation.result(180)

    print(u'Total Characters: {}'.format(result.total_characters))
    print(u'Translated Characters: {}'.format(result.translated_characters))
    # [END translate_batch_translate_text_beta]


def detect_language(project_id, text):
    # [START translate_detect_language_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = YOUR_PROJECT_ID
    # text = 'Text you wish to translate'
    location = 'global'

    parent = client.location_path(project_id, location)

    response = client.detect_language(
        parent=parent,
        content=text,
        mime_type='text/plain')  # mime types: text/plain, text/html

    for language in response.languages:
        print(u'Language Code: {} (Confidence: {})'.format(
            language.language_code,
            language.confidence))
    # [END translate_detect_language_beta]


def list_languages(project_id):
    # [START translate_list_codes_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = YOUR_PROJECT_ID
    location = 'global'

    parent = client.location_path(project_id, location)

    response = client.get_supported_languages(parent)

    print('Supported Languages:')
    for language in response.languages:
        print(u'Language Code: {}'.format(language.language_code))
    # [END translate_list_codes_beta]


def list_languages_with_target(project_id, display_language_code):
    # [START translate_list_language_names_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = YOUR_PROJECT_ID
    # display_language_code = 'is'
    location = 'global'

    parent = client.location_path(project_id, location)

    response = client.get_supported_languages(
        parent=parent,
        display_language_code=display_language_code)

    print('Supported Languages:')
    for language in response.languages:
        print(u'Language Code: {}'.format(language.language_code))
        print(u'Display Name: {}\n'.format(language.display_name))
    # [END translate_list_language_names_beta]


def create_glossary(project_id, glossary_id):
    # [START translate_create_glossary_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = 'YOUR_PROJECT_ID'
    # glossary_id = 'glossary-id'
    location = 'us-central1'  # The location of the glossary

    name = client.glossary_path(
        project_id,
        location,
        glossary_id)

    language_codes_set = translate.types.Glossary.LanguageCodesSet(
        language_codes=['en', 'es'])

    gcs_source = translate.types.GcsSource(
        input_uri='gs://cloud-samples-data/translation/glossary.csv')

    input_config = translate.types.GlossaryInputConfig(
        gcs_source=gcs_source)

    glossary = translate.types.Glossary(
        name=name,
        language_codes_set=language_codes_set,
        input_config=input_config)

    parent = client.location_path(project_id, location)

    operation = client.create_glossary(parent=parent, glossary=glossary)

    result = operation.result(timeout=90)
    print(u'Created: {}'.format(result.name))
    print(u'Input Uri: {}'.format(result.input_config.gcs_source.input_uri))
    # [END translate_create_glossary_beta]


def list_glossaries(project_id):
    # [START translate_list_glossary_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = 'YOUR_PROJECT_ID'
    location = 'us-central1'  # The location of the glossary

    parent = client.location_path(project_id, location)

    for glossary in client.list_glossaries(parent):
        print(u'Name: {}'.format(glossary.name))
        print(u'Entry count: {}'.format(glossary.entry_count))
        print(u'Input uri: {}'.format(
            glossary.input_config.gcs_source.input_uri))
        for language_code in glossary.language_codes_set.language_codes:
            print(u'Language code: {}'.format(language_code))
    # [END translate_list_glossary_beta]


def get_glossary(project_id, glossary_id):
    # [START translate_get_glossary_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = 'YOUR_PROJECT_ID'
    # glossary_id = 'GLOSSARY_ID'

    parent = client.glossary_path(
        project_id,
        'us-central1',  # The location of the glossary
        glossary_id)

    response = client.get_glossary(parent)
    print(u'Name: {}'.format(response.name))
    print(u'Language Pair:')
    print(u'\tSource Language Code: {}'.format(
        response.language_pair.source_language_code))
    print(u'\tTarget Language Code: {}'.format(
        response.language_pair.target_language_code))
    print(u'Input Uri: {}'.format(
        response.input_config.gcs_source.input_uri))
    # [END translate_get_glossary_beta]


def delete_glossary(project_id, glossary_id):
    # [START translate_delete_glossary_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = 'YOUR_PROJECT_ID'
    # glossary_id = 'GLOSSARY_ID'

    parent = client.glossary_path(
        project_id,
        'us-central1',  # The location of the glossary
        glossary_id)

    operation = client.delete_glossary(parent)
    result = operation.result(timeout=90)
    print(u'Deleted: {}'.format(result.name))
    # [END translate_delete_glossary_beta]


def translate_text_with_glossary(project_id, glossary_id, text):
    # [START translate_translate_text_with_glossary_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    # project_id = 'YOUR_PROJECT_ID'
    # glossary_id = 'GLOSSARY_ID'
    # text = 'Text you wish to translate'
    location = 'us-central1'  # The location of the glossary

    glossary = client.glossary_path(
        project_id,
        'us-central1',  # The location of the glossary
        glossary_id)

    glossary_config = translate.types.TranslateTextGlossaryConfig(
        glossary=glossary)

    parent = client.location_path(project_id, location)

    result = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='en',
        target_language_code='es',
        glossary_config=glossary_config)

    for translation in result.glossary_translations:
        print(translation)
    # [END translate_translate_text_with_glossary_beta]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    translate_text_parser = subparsers.add_parser(
        'translate-text', help=translate_text.__doc__)
    translate_text_parser.add_argument('project_id')
    translate_text_parser.add_argument('text')

    batch_translate_text_parser = subparsers.add_parser(
        'batch-translate-text', help=translate_text.__doc__)
    batch_translate_text_parser.add_argument('project_id')
    batch_translate_text_parser.add_argument('gcs_source')
    batch_translate_text_parser.add_argument('gcs_destination')

    detect_langage_parser = subparsers.add_parser(
        'detect-language', help=detect_language.__doc__)
    detect_langage_parser.add_argument('project_id')
    detect_langage_parser.add_argument('text')

    list_languages_parser = subparsers.add_parser(
        'list-languages', help=list_languages.__doc__)
    list_languages_parser.add_argument('project_id')

    list_languages_with_target_parser = subparsers.add_parser(
        'list-languages-with-target', help=list_languages_with_target.__doc__)
    list_languages_with_target_parser.add_argument('project_id')
    list_languages_with_target_parser.add_argument('display_language_code')

    create_glossary_parser = subparsers.add_parser(
        'create-glossary', help=create_glossary.__doc__)
    create_glossary_parser.add_argument('project_id')
    create_glossary_parser.add_argument('glossary_id')

    get_glossary_parser = subparsers.add_parser(
        'get-glossary', help=get_glossary.__doc__)
    get_glossary_parser.add_argument('project_id')
    get_glossary_parser.add_argument('glossary_id')

    list_glossary_parser = subparsers.add_parser(
        'list-glossaries', help=list_glossaries.__doc__)
    list_glossary_parser.add_argument('project_id')

    delete_glossary_parser = subparsers.add_parser(
        'delete-glossary', help=delete_glossary.__doc__)
    delete_glossary_parser.add_argument('project_id')
    delete_glossary_parser.add_argument('glossary_id')

    translate_with_glossary_parser = subparsers.add_parser(
        'translate-with-glossary', help=translate_text_with_glossary.__doc__)
    translate_with_glossary_parser.add_argument('project_id')
    translate_with_glossary_parser.add_argument('glossary_id')
    translate_with_glossary_parser.add_argument('text')

    args = parser.parse_args()

    if args.command == 'translate-text':
        translate_text(args.project_id, args.text)
    elif args.command == 'batch-translate-text':
        batch_translate_text(
            args.project_id, args.gcs_source, args.gcs_destination)
    elif args.command == 'detect-language':
        detect_language(args.project_id, args.text)
    elif args.command == 'list-languages':
        list_languages(args.project_id)
    elif args.command == 'list-languages-with-target':
        list_languages_with_target(args.project_id, args.display_language_code)
    elif args.command == 'create-glossary':
        create_glossary(args.project_id, args.glossary_id)
    elif args.command == 'get-glossary':
        get_glossary(args.project_id, args.glossary_id)
    elif args.command == 'list-glossaries':
        list_glossaries(args.project_id)
    elif args.command == 'delete-glossary':
        delete_glossary(args.project_id, args.glossary_id)
    elif args.command == 'translate-with-glossary':
        translate_text_with_glossary(
                args.project_id, args.glossary_id, args.text)
