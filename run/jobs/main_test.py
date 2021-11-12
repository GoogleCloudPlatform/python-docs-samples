# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess

import main


def test_main(capsys):
    main.main()
    out, _ = capsys.readouterr()
    expected = 'Completed Task #0.'
    assert expected in out


def test_env_vars():
    try:
        main.main(fail_rate='0.999999')
    except Exception as err:
        expected = 'failed'
        assert expected in str(err)


def test_bad_env_vars():
    try:
        main.main(fail_rate='2')
    except Exception as err:
        expected = 'Invalid'
        assert expected in str(err)


def test_run_script():
    output = (
        subprocess.run(
            ['python', 'main.py'],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    assert 'Completed' in output

    my_env = {'FAIL_RATE': '0.99999999'}
    try:
        subprocess.run(
            ['python', 'main.py'],
            env=my_env,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        assert 'non-zero' in str(err)
