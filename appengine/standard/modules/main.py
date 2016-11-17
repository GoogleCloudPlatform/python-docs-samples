# Copyright 2016 Google Inc. All rights reserved.
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

"""
Sample application that demonstrates getting information about this
AppEngine modules and accessing other modules in the same project.
"""

import urllib2
# [START modules_import]
from google.appengine.api import modules
# [END modules_import]
import webapp2


class GetModuleInfoHandler(webapp2.RequestHandler):
    def get(self):
        # [START module_info]
        module = modules.get_current_module_name()
        instance_id = modules.get_current_instance_id()
        self.response.write(
            'module_id={}&instance_id={}'.format(module, instance_id))
        # [END module_info]


class GetBackendHandler(webapp2.RequestHandler):
    def get(self):
        # [START access_another_module]
        backend_hostname = modules.get_hostname(module='my-backend')
        url = "http://{}/".format(backend_hostname)
        try:
            result = urllib2.urlopen(url).read()
            self.response.write('Got response {}'.format(result))
        except urllib2.URLError:
            pass
        # [END access_another_module]


app = webapp2.WSGIApplication([
    ('/', GetModuleInfoHandler),
    ('/access_backend', GetBackendHandler),
], debug=True)
