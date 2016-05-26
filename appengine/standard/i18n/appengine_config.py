#!/usr/bin/env python
#
# Copyright 2013 Google Inc.
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

"""App Engine configuration file for applying the I18nMiddleware."""


from i18n_utils import I18nMiddleware


def webapp_add_wsgi_middleware(app):
    """Applying the I18nMiddleware to our HelloWorld app.

    Args:
        app: The WSGI application object that you want to wrap with the
            I18nMiddleware.

    Returns:
        The wrapped WSGI application.
    """

    app = I18nMiddleware(app)
    return app
