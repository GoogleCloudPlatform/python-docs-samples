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

"""Sample application that demonstrates how to internationalize and localize
and App Engine application.

For more information, see README.md
"""

import webapp2

from i18n_utils import BaseHandler


class MainHandler(BaseHandler):
    """A simple handler with internationalized strings.

    This handler demonstrates how to internationalize strings in
    Python, Jinja2 template and Javascript.
    """

    def get(self):
        """A get handler for this sample.

        It just shows internationalized strings in Python, Jinja2
        template and Javascript.
        """

        context = dict(message=gettext('Hello World from Python code!'))
        template = self.jinja2_env.get_template('index.jinja2')
        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
