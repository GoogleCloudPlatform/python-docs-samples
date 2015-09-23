# Copyright 2010 Google Inc. All Rights Reserved.

"""
Manages the namespace for the application.

This file presents ways an ISV (Independent Software Vendor) might use
namespaces to distribute the guestbook application to different corporate
clients. The original guestbook.py is left unchanged. Our namespace choosing
hook is run when datastore or memcache attempt to resolve the namespace.
When defined in appengine_config.py the lib_config mechanism substitutes this
function for the default definition which returns None. This hopefully shows
how easy it can be to make an existing app namespace aware.

Setting _NAMESPACE_PICKER has the following effects:

If _USE_SERVER_NAME, we read the server name
foo.guestbook-isv.appspot.com and set the namespace.

If _USE_GOOGLE_APPS_DOMAIN, we allow the namespace manager to infer the
namespace from the request.

If _USE_COOKIE, then the ISV might have a gateway page that sets a cookie
called 'namespace' for example, and we read this cookie and set the namespace
to its value.  Note this is not a secure use of cookies.

Other possibilities not implemented here include using a mapping from user to
namespace and possibly setting a namespace cookie from this mapping. If the
mapping is stored in datastore, we would probably not wish to look it up on
every query.
"""

__author__ = 'nverne@google.com (Nicholas Verne)'


import Cookie
import os

from google.appengine.api import namespace_manager


_USE_SERVER_NAME = 0
_USE_GOOGLE_APPS_DOMAIN = 1
_USE_COOKIE = 2

_NAMESPACE_PICKER = _USE_SERVER_NAME


def namespace_manager_default_namespace_for_request():
    """Determine which namespace is to be used for a request.

    The value of _NAMESPACE_PICKER has the following effects:

    If _USE_SERVER_NAME, we read server name
    foo.guestbook-isv.appspot.com and set the namespace.

    If _USE_GOOGLE_APPS_DOMAIN, we allow the namespace manager to infer
    the namespace from the request.

    If _USE_COOKIE, then the ISV might have a gateway page that sets a
    cookie called 'namespace', and we set the namespace to the cookie's value
    """
    name = None

    if _NAMESPACE_PICKER == _USE_SERVER_NAME:
        name = os.environ['SERVER_NAME']
    elif _NAMESPACE_PICKER == _USE_GOOGLE_APPS_DOMAIN:
        name = namespace_manager.google_apps_namespace()
    elif _NAMESPACE_PICKER == _USE_COOKIE:
        cookies = os.getenv('HTTP_COOKIE', None)
        if cookies:
            name = Cookie.BaseCookie(cookies).get('namespace')

    return name
