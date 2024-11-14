# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import os
import re
import subprocess
import sys
import textwrap
import uuid
from collections.abc import Callable, Iterable
from datetime import datetime
from typing import AsyncIterator

import pytest
import pytest_asyncio


def get_env_var(key: str) -> str:
    v = os.environ.get(key)
    if v is None:
        raise ValueError(f"Must set env var {key}")
    return v


@pytest.fixture(scope="session")
def table_name() -> str:
    return "investments"


@pytest.fixture(scope="session")
def cluster_name() -> str:
    return get_env_var("ALLOYDB_CLUSTER")


@pytest.fixture(scope="session")
def instance_name() -> str:
    return get_env_var("ALLOYDB_INSTANCE")


@pytest.fixture(scope="session")
def region() -> str:
    return get_env_var("ALLOYDB_REGION")


@pytest.fixture(scope="session")
def database_name() -> str:
    return get_env_var("ALLOYDB_DATABASE_NAME")


@pytest.fixture(scope="session")
def password() -> str:
    return get_env_var("ALLOYDB_PASSWORD")


@pytest_asyncio.fixture(scope="session")
def project_id() -> str:
    gcp_project = get_env_var("GOOGLE_CLOUD_PROJECT")
    run_cmd("gcloud", "config", "set", "project", gcp_project)
    # Since everything requires the project, let's confiugre and show some
    # debugging information here.
    run_cmd("gcloud", "version")
    run_cmd("gcloud", "config", "list")
    return gcp_project


def run_cmd(*cmd: str) -> subprocess.CompletedProcess:
    try:
        print(f">> {cmd}")
        start = datetime.now()
        p = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(p.stderr.decode("utf-8"))
        print(p.stdout.decode("utf-8"))
        elapsed = (datetime.now() - start).seconds
        minutes = int(elapsed / 60)
        seconds = elapsed - minutes * 60
        print(f"Command `{cmd[0]}` finished in {minutes}m {seconds}s")
        return p
    except subprocess.CalledProcessError as e:
        # Include the error message from the failed command.
        print(e.stderr.decode("utf-8"))
        print(e.stdout.decode("utf-8"))
        raise RuntimeError(f"{e}\n\n{e.stderr.decode('utf-8')}") from e


def run_notebook(
    ipynb_file: str,
    prelude: str = "",
    section: str = "",
    variables: dict = {},
    replace: dict[str, str] = {},
    preprocess: Callable[[str], str] = lambda source: source,
    skip_shell_commands: bool = False,
    until_end: bool = False,
) -> None:
    import nbformat
    from nbclient.client import NotebookClient
    from nbclient.exceptions import CellExecutionError

    def notebook_filter_section(
        start: str,
        end: str,
        cells: list[nbformat.NotebookNode],
        until_end: bool = False,
    ) -> Iterable[nbformat.NotebookNode]:
        in_section = False
        for cell in cells:
            if cell["cell_type"] == "markdown":
                if not in_section and cell["source"].startswith(start):
                    in_section = True
                elif in_section and not until_end and cell["source"].startswith(end):
                    return
            if in_section:
                yield cell

    # Regular expression to match and remove shell commands from the notebook.
    #   https://regex101.com/r/EHWBpT/1
    shell_command_re = re.compile(r"^!((?:[^\n]+\\\n)*(?:[^\n]+))$", re.MULTILINE)
    # Compile regular expressions for variable substitutions.
    #   https://regex101.com/r/e32vfW/1
    compiled_substitutions = [
        (
            re.compile(rf"""\b{name}\s*=\s*(?:f?'[^']*'|f?"[^"]*"|\w+)"""),
            f"{name} = {repr(value)}",
        )
        for name, value in variables.items()
    ]
    # Filter the section if any, otherwise use the entire notebook.
    nb = nbformat.read(ipynb_file, as_version=4)
    if section:
        start = section
        end = section.split(" ", 1)[0] + " "
        nb.cells = list(notebook_filter_section(start, end, nb.cells, until_end))
        if len(nb.cells) == 0:
            raise ValueError(
                f"Section {repr(section)} not found in notebook {repr(ipynb_file)}"
            )
    # Preprocess the cells.
    for cell in nb.cells:
        # Only preprocess code cells.
        if cell["cell_type"] != "code":
            continue
        # Run any custom preprocessing functions before.
        cell["source"] = preprocess(cell["source"])
        # Preprocess shell commands.
        if skip_shell_commands:
            cmd = "pass"
            cell["source"] = shell_command_re.sub(cmd, cell["source"])
        else:
            cell["source"] = shell_command_re.sub(r"_run(f'''\1''')", cell["source"])
        # Apply variable substitutions.
        for regex, new_value in compiled_substitutions:
            cell["source"] = regex.sub(new_value, cell["source"])
        # Apply replacements.
        for old, new in replace.items():
            cell["source"] = cell["source"].replace(old, new)
        # Clear outputs.
        cell["outputs"] = []
    # Prepend the prelude cell.
    prelude_src = textwrap.dedent(
        """\
        def _run(cmd):
            import subprocess as _sp
            import sys as _sys
            _p = _sp.run(cmd, shell=True, stdout=_sp.PIPE, stderr=_sp.PIPE)
            _stdout = _p.stdout.decode('utf-8').strip()
            _stderr = _p.stderr.decode('utf-8').strip()
            if _stdout:
                print(f'➜ !{cmd}')
                print(_stdout)
            if _stderr:
                print(f'➜ !{cmd}', file=_sys.stderr)
                print(_stderr, file=_sys.stderr)
            if _p.returncode:
                raise RuntimeError('\\n'.join([
                    f"Command returned non-zero exit status {_p.returncode}.",
                    f"-------- command --------",
                    f"{cmd}",
                    f"-------- stderr --------",
                    f"{_stderr}",
                    f"-------- stdout --------",
                    f"{_stdout}",
                ]))
        """
        + prelude
    )
    nb.cells = [nbformat.v4.new_code_cell(prelude_src)] + nb.cells
    # Run the notebook.
    error = ""
    client = NotebookClient(nb)
    try:
        client.execute()
    except CellExecutionError as e:
        # Remove colors and other escape characters to make it easier to read in the logs.
        #   https://stackoverflow.com/a/33925425
        color_chars = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        error = color_chars.sub("", str(e))
        for cell in nb.cells:
            if cell["cell_type"] != "code":
                continue
            for output in cell["outputs"]:
                if output.get("name") == "stdout":
                    print(color_chars.sub("", output["text"]))
                elif output.get("name") == "stderr":
                    print(color_chars.sub("", output["text"]), file=sys.stderr)
    if error:
        raise RuntimeError(
            f"Error on {repr(ipynb_file)}, section {repr(section)}: {error}"
        )
