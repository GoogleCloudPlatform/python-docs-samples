# App Engine Internationalization Sample

A simple example app showing how to build an internationalized app
with App Engine.

## What to internationalize

There are lots of things to internationalize with your web
applications.

1.  Strings in Python code
2.  Strings in HTML template
3.  Strings in Javascript
4.  Common strings
    - Country Names, Language Names, etc.
5.  Formatting
    - Date/Time formatting
    - Number formatting
    - Currency
6.  Timezone conversion

This example only covers first 3 basic scenarios above. In order to
cover other aspects, I recommend using
[Babel](http://babel.edgewall.org/) and [pytz]
(http://pypi.python.org/pypi/gaepytz). Also, you may want to use
[webapp2_extras.i18n](http://webapp-improved.appspot.com/tutorials/i18n.html)
module.

## Wait, so why not webapp2_extras.i18n?

webapp2_extras.i18n doesn't cover how to internationalize strings in
Javascript code. Additionally it depends on babel and pytz, which
means you need to deploy babel and pytz alongside with your code. I'd
like to show a reasonably minimum example for string
internationalization in Python code, jinja2 templates, as well as
Javascript.

## How to run this example

First of all, please install babel in your local Python environment.

### Wait, you just said I don't need babel, are you crazy?

As I said before, you don't need to deploy babel with this
application, but you need to locally use pybabel script which is
provided by babel distribution in order to extract the strings, manage
and compile the translations file.

### Extract strings in Python code and Jinja2 templates to translate

Move into this project directory and invoke the following command:

    $ env PYTHONPATH=/google_appengine_sdk/lib/jinja2 \
        pybabel extract -o locales/messages.pot -F main.mapping .

This command creates a `locales/messages.pot` file in the `locales`
directory which contains all the string found in your Python code and
Jija2 tempaltes.

Since the babel configration file `main.mapping` contains a reference
to `jinja2.ext.babel_extract` helper function which is provided by
jinja2 distribution bundled with the App Engine SDK, you need to add a
PYTHONPATH environment variable pointing to the jinja2 directory in
the SDK.

### Manage and compile translations.

Create an initial translation source by the following command:

    $ pybabel init -l ja -d locales -i locales/messages.pot

Open `locales/ja/LC_MESSAGES/messages.po` with any text editor and
translate the strings, then compile the file by the following command:

    $ pybabel compile -d locales

If any of the strings changes, you can extract the strings again, and
update the translations by the following command:

    $ pybabel update -l ja -d locales -i locales/messages.pot

Note: If you run `pybabel init` against an existant translations file,
you will lose your translations.


### Extract strings in Javascript code and compile translations

    $ pybabel extract -o locales/jsmessages.pot -F js.mapping .
    $ pybabel init -l ja -d locales -i locales/jsmessages.pot -D jsmessages

Open `locales/ja/LC_MESSAGES/jsmessages.po` and translate it.

    $ pybabel compile -d locales -D jsmessages

### Running locally & deploying

Refer to the [App Engine Samples README](../README.md) for information on how to run and deploy this sample.

## How it works

As you can see it in the `appengine_config.py` file, our
`main.application` is wrapped by the `i18n_utils.I18nMiddleware` WSGI
middleware. When a request comes in, this middleware parses the
`HTTP_ACCEPT_LANGUAGE` HTTP header, loads available translation
files(`messages.mo`) from the application directory, and install the
`gettext` and `ngettext` functions to the `__builtin__` namespace in
the Python runtime.

For strings in Jinja2 templates, there is the `i18n_utils.BaseHandler`
class from which you can extend in order to have a handy property
named `jinja2_env` that lazily initializes Jinja2 environment for you
with the `jinja2.ext.i18n` extention, and similar to the
`I18nMiddleware`, installs `gettext` and `ngettext` functions to the
global namespace of the Jinja2 environment.

## What about Javascript?

The `BaseHandler` class also installs the `get_i18n_js_tag()` instance
method to the Jinja2 global namespace. When you use this function in
your Jinja2 template (like in the `index.jinja2` file), you will get a
set of Javascript functions; `gettext`, `ngettext`, and `format` on
the string type. The `format` function can be used with `ngettext`ed
strings for number formatting. See this example:

    window.alert(ngettext(
        'You need to provide at least {0} item.',
        'You need to provide at least {0} items.',
        n).format(n);
