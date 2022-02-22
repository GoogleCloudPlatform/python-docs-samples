# Copyright 2022 Google LLC.
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

import pytest

import main


def test_main(capsys):
    main.main()
    out, _ = capsys.readouterr()
    expected = "Completed Task #0."
    assert expected in out


def test_env_vars():
    with pytest.raises(Exception, match=r".*failed.*"):
        main.main(fail_rate="0.999999")


def test_bad_env_vars(capsys):
    main.main(fail_rate="2")  # Does not fail, so retry is not triggered
    out, _ = capsys.readouterr()
    assert "Invalid FAIL_RATE env var value" in out


def test_run_script():
    output = (
        subprocess.run(
            ["python3", "main.py"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    assert "Completed" in output

    my_env = {"FAIL_RATE": "0.99999999"}
    with pytest.raises(subprocess.CalledProcessError, match=r".*non-zero.*"):
        subprocess.run(
            ["python3", "main.py"],
            env=my_env,
            stderr=subprocess.PIPE,
            check=True,
        )
