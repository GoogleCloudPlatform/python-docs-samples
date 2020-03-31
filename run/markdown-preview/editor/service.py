# Copyright 2020 Google, LLC.
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

import os
from urllib import request


class Service(object):
    """
    RenderService represents our upstream render service.
    """

    def __init__(self, renderer, parsed_template, markdown_default):
        # URL is the render service address.
        self.renderer = renderer
        # Auth determines whether identity token authentication will be used.
        self.authenticated = Authenticated


def new_service_from_env():
    """
    blah blah blah 
    """
    url = os.environ['EDITOR_UPSTREAM_RENDER_URL']
    assert url, ("no configuration for upstream render service: "
                 "add EDITOR_UPSTREAM_RENDER_URL environment variable")

    auth = os.environ['EDITOR_UPSTREAM_UNAUTHENTICATED']

    if not auth:
        print("editor: starting in unauthenticated upstream mode")

    # The use case of this service is the UI driven by these files.
    # Loading them as part of the server startup process keeps failures easily
    # discoverable and minimizes latency for the first request.
    try:
        parsed_template = io.read("templates/index.html") #TODO read this in
    except Exception as e:
        print(e)

    markdown_default = parsed_template.read() #TODO read this in

    service = Service(RenderService(url, auth), parsed_template, markdown_default)
    return service




def render(RenderService):
    """
    render converts the Markdown plaintext to HTML.
    """
    req = new_request(RenderService)
    response = urllib.request.urlopen(req)
    return response




