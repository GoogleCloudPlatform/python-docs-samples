# Copyright 2016, Google, Inc.
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

import textwrap

import analyze


def test_analyze_entities():
    result = analyze.analyze_entities(
        'Tom Sawyer is a book written by a guy known as Mark Twain.')

    assert result['language'] == 'en'
    entities = result['entities']
    assert len(entities)
    subject = entities[0]
    assert subject['type'] == 'PERSON'
    assert subject['name'].startswith('Tom')


def test_analyze_sentiment(capsys):
    result = analyze.analyze_sentiment(
        'your face is really ugly and i hate it.')

    sentiment = result['documentSentiment']
    assert sentiment['score'] < 0
    assert sentiment['magnitude'] < 1

    result = analyze.analyze_sentiment(
        'cheerio, mate - I greatly admire the pallor of your visage, and your '
        'angle of repose leaves little room for improvement.')

    sentiment = result['documentSentiment']
    assert sentiment['score'] > 0
    assert sentiment['magnitude'] < 1


def test_analyze_syntax(capsys):
    result = analyze.analyze_syntax(textwrap.dedent(u'''\
        Keep away from people who try to belittle your ambitions. Small people
        always do that, but the really great make you feel that you, too, can
        become great.
        - Mark Twain'''))

    assert len(result['tokens'])
    first_token = result['tokens'][0]
    assert first_token['text']['content'] == 'Keep'
    assert first_token['partOfSpeech']['tag'] == 'VERB'
    assert len(result['sentences']) > 1
    assert result['language'] == 'en'


def test_analyze_syntax_utf8():
    """Demonstrate the interpretation of the offsets when encoding=utf8.

    UTF8 is a variable-length encoding, where each character is at least 8
    bits. The offsets we get should be the index of the first byte of the
    character.
    """
    test_string = u'a \u00e3 \u0201 \U0001f636 b'
    byte_array = test_string.encode('utf8')
    result = analyze.analyze_syntax(test_string, encoding='UTF8')
    tokens = result['tokens']

    assert tokens[0]['text']['content'] == 'a'
    offset = tokens[0]['text'].get('beginOffset', 0)
    assert (byte_array[offset:offset+1].decode('utf8') ==
            tokens[0]['text']['content'])

    assert tokens[1]['text']['content'] == u'\u00e3'
    offset = tokens[1]['text'].get('beginOffset', 0)
    assert (byte_array[offset:offset+2].decode('utf8') ==
            tokens[1]['text']['content'])

    assert tokens[2]['text']['content'] == u'\u0201'
    offset = tokens[2]['text'].get('beginOffset', 0)
    assert (byte_array[offset:offset+2].decode('utf8') ==
            tokens[2]['text']['content'])

    assert tokens[3]['text']['content'] == u'\U0001f636'
    offset = tokens[3]['text'].get('beginOffset', 0)
    assert (byte_array[offset:offset+4].decode('utf8') ==
            tokens[3]['text']['content'])

    # This demonstrates that the offset takes into account the variable-length
    # characters before the target token.
    assert tokens[4]['text']['content'] == u'b'
    offset = tokens[4]['text'].get('beginOffset', 0)
    # 'b' is only one byte long
    assert (byte_array[offset:offset+1].decode('utf8') ==
            tokens[4]['text']['content'])


def test_analyze_syntax_utf16():
    """Demonstrate the interpretation of the offsets when encoding=utf16.

    UTF16 is a variable-length encoding, where each character is at least 16
    bits. The returned offsets will be the index of the first 2-byte character
    of the token.
    """
    test_string = u'a \u00e3 \u0201 \U0001f636 b'
    byte_array = test_string.encode('utf16')
    # Remove the byte order marker, which the offsets don't account for
    byte_array = byte_array[2:]
    result = analyze.analyze_syntax(test_string, encoding='UTF16')
    tokens = result['tokens']

    assert tokens[0]['text']['content'] == 'a'
    # The offset is an offset into an array where each entry is 16 bits. Since
    # we have an 8-bit array, the offsets should be doubled to index into our
    # array.
    offset = 2 * tokens[0]['text'].get('beginOffset', 0)
    assert (byte_array[offset:offset + 2].decode('utf16') ==
            tokens[0]['text']['content'])

    assert tokens[1]['text']['content'] == u'\u00e3'
    offset = 2 * tokens[1]['text'].get('beginOffset', 0)
    # A UTF16 character with a low codepoint is 16 bits (2 bytes) long, so
    # slice out 2 bytes starting from the offset. Then interpret the bytes as
    # utf16 for comparison.
    assert (byte_array[offset:offset + 2].decode('utf16') ==
            tokens[1]['text']['content'])

    assert tokens[2]['text']['content'] == u'\u0201'
    offset = 2 * tokens[2]['text'].get('beginOffset', 0)
    # A UTF16 character with a low codepoint is 16 bits (2 bytes) long, so
    # slice out 2 bytes starting from the offset. Then interpret the bytes as
    # utf16 for comparison.
    assert (byte_array[offset:offset + 2].decode('utf16') ==
            tokens[2]['text']['content'])

    assert tokens[3]['text']['content'] == u'\U0001f636'
    offset = 2 * tokens[3]['text'].get('beginOffset', 0)
    # A UTF16 character with a high codepoint is 32 bits (4 bytes) long, so
    # slice out 4 bytes starting from the offset. Then interpret those bytes as
    # utf16 for comparison.
    assert (byte_array[offset:offset + 4].decode('utf16') ==
            tokens[3]['text']['content'])

    # This demonstrates that the offset takes into account the variable-length
    # characters before the target token.
    assert tokens[4]['text']['content'] == u'b'
    offset = 2 * tokens[4]['text'].get('beginOffset', 0)
    # Even though 'b' is only one byte long, utf16 still encodes it using 16
    # bits
    assert (byte_array[offset:offset + 2].decode('utf16') ==
            tokens[4]['text']['content'])


def test_annotate_text_utf32():
    """Demonstrate the interpretation of the offsets when encoding=utf32.

    UTF32 is a fixed-length encoding, where each character is exactly 32 bits.
    The returned offsets will be the index of the first 4-byte character
    of the token.

    Python unicode objects index by the interpreted unicode character. This
    means a given unicode character only ever takes up one slot in a unicode
    string. This is equivalent to indexing into a UTF32 string, where all
    characters are a fixed length and thus will only ever take up one slot.

    Thus, if you're indexing into a python unicode object, you can set
    encoding to UTF32 to index directly into the unicode object (as opposed to
    the byte arrays, as these examples do).

    Nonetheless, this test still demonstrates indexing into the byte array, for
    consistency. Note that you could just index into the origin test_string
    unicode object with the raw offset returned by the api (ie without
    multiplying it by 4, as it is below).
    """
    test_string = u'a \u00e3 \u0201 \U0001f636 b'
    byte_array = test_string.encode('utf32')
    # Remove the byte order marker, which the offsets don't account for
    byte_array = byte_array[4:]
    result = analyze.analyze_syntax(test_string, encoding='UTF32')
    tokens = result['tokens']

    assert tokens[0]['text']['content'] == 'a'
    # The offset is an offset into an array where each entry is 32 bits. Since
    # we have an 8-bit array, the offsets should be quadrupled to index into
    # our array.
    offset = 4 * tokens[0]['text'].get('beginOffset', 0)
    assert (byte_array[offset:offset + 4].decode('utf32') ==
            tokens[0]['text']['content'])

    assert tokens[1]['text']['content'] == u'\u00e3'
    offset = 4 * tokens[1]['text'].get('beginOffset', 0)
    # A UTF32 character with a low codepoint is 32 bits (4 bytes) long, so
    # slice out 4 bytes starting from the offset. Then interpret the bytes as
    # utf32 for comparison.
    assert (byte_array[offset:offset + 4].decode('utf32') ==
            tokens[1]['text']['content'])

    assert tokens[2]['text']['content'] == u'\u0201'
    offset = 4 * tokens[2]['text'].get('beginOffset', 0)
    # A UTF32 character with a low codepoint is 32 bits (4 bytes) long, so
    # slice out 4 bytes starting from the offset. Then interpret the bytes as
    # utf32 for comparison.
    assert (byte_array[offset:offset + 4].decode('utf32') ==
            tokens[2]['text']['content'])

    assert tokens[3]['text']['content'] == u'\U0001f636'
    offset = 4 * tokens[3]['text'].get('beginOffset', 0)
    # A UTF32 character with a high codepoint is 32 bits (4 bytes) long, so
    # slice out 4 bytes starting from the offset. Then interpret those bytes as
    # utf32 for comparison.
    assert (byte_array[offset:offset + 4].decode('utf32') ==
            tokens[3]['text']['content'])

    # This demonstrates that the offset takes into account the variable-length
    # characters before the target token.
    assert tokens[4]['text']['content'] == u'b'
    offset = 4 * tokens[4]['text'].get('beginOffset', 0)
    # Even though 'b' is only one byte long, utf32 still encodes it using 32
    # bits
    assert (byte_array[offset:offset + 4].decode('utf32') ==
            tokens[4]['text']['content'])


def test_annotate_text_utf32_directly_index_into_unicode():
    """Demonstrate using offsets directly, using encoding=utf32.

    See the explanation for test_annotate_text_utf32. Essentially, indexing
    into a utf32 array is equivalent to indexing into a python unicode object.
    """
    test_string = u'a \u00e3 \u0201 \U0001f636 b'
    result = analyze.analyze_syntax(test_string, encoding='UTF32')
    tokens = result['tokens']

    assert tokens[0]['text']['content'] == 'a'
    offset = tokens[0]['text'].get('beginOffset', 0)
    assert test_string[offset] == tokens[0]['text']['content']

    assert tokens[1]['text']['content'] == u'\u00e3'
    offset = tokens[1]['text'].get('beginOffset', 0)
    assert test_string[offset] == tokens[1]['text']['content']

    assert tokens[2]['text']['content'] == u'\u0201'
    offset = tokens[2]['text'].get('beginOffset', 0)
    assert test_string[offset] == tokens[2]['text']['content']

    # Temporarily disabled
    # assert tokens[3]['text']['content'] == u'\U0001f636'
    # offset = tokens[3]['text'].get('beginOffset', 0)
    # assert test_string[offset] == tokens[3]['text']['content']

    # assert tokens[4]['text']['content'] == u'b'
    # offset = tokens[4]['text'].get('beginOffset', 0)
    # assert test_string[offset] == tokens[4]['text']['content']
