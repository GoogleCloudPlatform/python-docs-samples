<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud Platform logo" title="Google Cloud Platform" align="right" height="96" width="96"/>

# Google Translate API Python Samples

With the [Google Translate API][translate_docs], you can dynamically translate
text between thousands of language pairs.

[translate_docs]: https://cloud.google.com/translate/docs/

## Table of Contents

* [Setup](#setup)
* [Samples](#samples)
  * [Translate](#translate)

## Setup

You will need to enable the Translate API and acquire and API key. See the
[documentation][translate_docs] for details on how to do this.

Install dependencies:

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

## Samples

### Translate

View the [documentation][translate_docs] or the [source code][translate_code].

__Usage:__ `python snippets.py --help`

```
usage: snippets.py [-h]
                   api_key
                   {detect-language,list-languages,list-languages-with-target,translate-text}
                   ...

This application demonstrates how to perform basic operations with the
Google Cloud Translate API

For more information, the documentation at
https://cloud.google.com/translate/docs.

positional arguments:
  api_key               Your API key.
  {detect-language,list-languages,list-languages-with-target,translate-text}
    detect-language     Detects the text's language.
    list-languages      Lists all available langauges.
    list-languages-with-target
                        Lists all available langauges and localizes them to
                        the target language. Target must be an ISO 639-1
                        language code.
    translate-text      Translates text into the target language. Target must
                        be an ISO 639-1 language code.

optional arguments:
  -h, --help            show this help message and exit
```

[translate_docs]: https://cloud.google.com/translate/docs
[translate_code]: snippets.py
