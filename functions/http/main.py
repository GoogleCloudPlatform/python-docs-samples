# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_http_xml]
import json
# [END functions_http_xml]

# [START functions_http_form_data]
import os
import tempfile
# [END functions_http_form_data]

# [START functions_http_form_data]
from werkzeug.utils import secure_filename
# [END functions_http_form_data]

# [START functions_http_xml]
import xmltodict
# [END functions_http_xml]


# [START functions_http_xml]

def parse_xml(request):
    data = xmltodict.parse(request.data)
    return json.dumps(data, indent=2)
# [END functions_http_xml]


# [START functions_http_form_data]

# Helper function that computes the filepath to save files to
def get_file_path(filename):
    # Note: tempfile.gettempdir() points to an in-memory file system
    # on GCF. Thus, any files in it must fit in the instance's memory.
    file_name = secure_filename(filename)
    return os.path.join(tempfile.gettempdir(), file_name)


def parse_multipart(request):
    # This code will process each non-file field in the form
    fields = {}
    data = request.form.to_dict()
    for field in data:
        fields[field] = data[field]
        print 'Processed field: %s' % field

    # This code will process each file uploaded
    files = request.files.to_dict()
    for file_name, file in files.iteritems():
        file.save(get_file_path(file_name))
        print 'Processed file: %s' % file_name

    # Clear temporary directory
    for file_name in files:
        file_path = get_file_path(file_name)
        os.remove(file_path)

    return "Done!"
# [END functions_http_form_data]
