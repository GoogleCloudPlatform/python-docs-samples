# Copyright 2021 Google LLC
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

import datetime
import os
from os.path import isdir, isfile, join
import signal

from flask import abort, Flask, redirect

app = Flask(__name__)

# Set config for file system path and filename prefix
mnt_dir = os.environ.get('MNT_DIR', '/mnt/nfs/filestore')
filename = os.environ.get('FILENAME', 'test')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Redirects to the file system path to interact with file system
    Writes a new file on each request
    """
    # Redirect to mount path
    path = '/' + path
    if (not path.startswith(mnt_dir)):
        return redirect(mnt_dir)

    # Add parent mount path link
    html = '<html><body>\n'
    if (path != mnt_dir):
        html += f'<a href=\"{mnt_dir}\">{mnt_dir}</a><br/><br/>\n'
    else:
        # Write a new test file
        try:
            write_file(mnt_dir, filename)
        except Exception:
            abort(500, description='Error writing file.')

    # Return all files if path is a directory, else return the file
    if (isdir(path)):
        for file in os.listdir(path):
            full_path = join(path, file)
            if isfile(full_path):
                html += f'<a href=\"{full_path}\">{file}</a><br/>\n'
    else:
        try:
            html += read_file(path)
        except Exception:
            abort(404, description='Error retrieving file.')

    html += '</body></html>\n'
    return html


def write_file(mnt_dir, filename):
    '''Write files to a directory with date created'''
    date = datetime.datetime.utcnow()
    file_date = '{dt:%a}-{dt:%b}-{dt:%d}-{dt:%H}:{dt:%M}-{dt:%Y}'.format(dt=date)
    with open(f'{mnt_dir}/{filename}-{file_date}.txt', 'a') as f:
        f.write(f'This test file was created on {date}.')


def read_file(full_path):
    '''Read files and return contents'''
    with open(full_path) as reader:
        return reader.read()


def shutdown_handler(signal, frame):
    '''SIGTERM handler'''
    print('Caught SIGTERM signal.', flush=True)
    return


# Register SIGTERM handler
signal.signal(signal.SIGTERM, shutdown_handler)

# To locally run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
