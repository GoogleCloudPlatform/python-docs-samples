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

from datetime import datetime
import multiprocessing
import os
import platform
import re
import subprocess
from unittest import mock
import uuid
from collections.abc import Callable, Iterable

from google.cloud import storage
import pytest


@pytest.fixture(scope="session")
def project() -> str:
    # This is set by the testing infrastructure.
    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    run_cmd("gcloud", "config", "set", "project", project)

    # Since everything requires the project, let's confiugre and show some
    # debugging information here.
    run_cmd("gcloud", "version")
    run_cmd("gcloud", "config", "list")
    return project


@pytest.fixture(scope="session")
def location() -> str:
    # Override for local testing.
    return os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")


@pytest.fixture(scope="session")
def python_version() -> str:
    return "".join(platform.python_version_tuple()[0:2])


@pytest.fixture(scope="session")
def unique_id() -> str:
    id = uuid.uuid4().hex[0:6]
    print(f"Test unique identifier: {id}")
    return id


@pytest.fixture(scope="session")
def unique_name(test_name: str, unique_id: str) -> str:
    return f"{test_name.replace('/', '-')}-{unique_id}"


@pytest.fixture(scope="session")
def bucket_name(test_name: str, location: str, unique_id: str) -> Iterable[str]:
    # Override for local testing.
    if "GOOGLE_CLOUD_BUCKET" in os.environ:
        bucket_name = os.environ["GOOGLE_CLOUD_BUCKET"]
        print(f"bucket_name: {bucket_name} (from GOOGLE_CLOUD_BUCKET)")
        yield bucket_name
        return

    storage_client = storage.Client()
    bucket_name = f"{test_name.replace('/', '-')}-{unique_id}"
    bucket = storage_client.create_bucket(bucket_name, location=location)

    print(f"bucket_name: {bucket_name}")
    yield bucket_name

    # Try to remove all files before deleting the bucket.
    # Deleting a bucket with too many files results in an error.
    try:
        run_cmd("gsutil", "-m", "rm", "-rf", f"gs://{bucket_name}/*")
    except RuntimeError:
        # If no files were found and it fails, ignore the error.
        pass

    # Delete the bucket.
    bucket.delete(force=True)


@pytest.fixture(scope="session")
# Disable printing to not log the identity token.
@mock.patch("builtins.print", lambda x: x)
def identity_token() -> str:
    return (
        run_cmd("gcloud", "auth", "print-identity-token").stdout.decode("utf-8").strip()
    )


def env_var(prefix: str, id: str = "") -> str:
    return f"{prefix}_{id}".replace(".", "").replace("/", "").strip("_")


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


def cloud_run_cleanup(service_name: str, location: str) -> None:
    # Delete the Container Registry image associated with the service.
    image = (
        run_cmd(
            "gcloud",
            "run",
            "services",
            "describe",
            service_name,
            f"--region={location}",
            "--format=get(image)",
        )
        .stdout.decode("utf-8")
        .strip()
    )
    run_cmd(
        "gcloud",
        "container",
        "images",
        "delete",
        image,
        "--force-delete-tags",
        "--quiet",
    )

    # Delete the Cloud Run service.
    run_cmd(
        "gcloud",
        "run",
        "services",
        "delete",
        service_name,
        f"--region={location}",
        "--quiet",
    )


def aiplatform_cleanup(model_name: str, location: str, versions: list[str]) -> None:
    # Delete versions.
    for version in versions:
        run_cmd(
            "gcloud",
            "ai-platform",
            "versions",
            "delete",
            version,
            f"--model={model_name}",
            f"--region={location}",
            "--quiet",
        )

    # Delete model.
    run_cmd(
        "gcloud",
        "ai-platform",
        "models",
        "delete",
        model_name,
        f"--region={location}",
        "--quiet",
    )


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
    from nbclient.client import NotebookClient
    from nbclient.exceptions import CellExecutionError
    import nbformat

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
            cmd = [
                "import subprocess",
                "_cmd = f'''\\1'''",
                "print(f'>> {_cmd}')",
                "subprocess.run(_cmd, shell=True, check=True)",
            ]
            cell["source"] = shell_command_re.sub("\n".join(cmd), cell["source"])

        # Apply variable substitutions.
        for regex, new_value in compiled_substitutions:
            cell["source"] = regex.sub(new_value, cell["source"])

        # Apply replacements.
        for old, new in replace.items():
            cell["source"] = cell["source"].replace(old, new)

    # Prepend the prelude cell.
    nb.cells = [nbformat.v4.new_code_cell(prelude)] + nb.cells

    # Run the notebook.
    error = ""
    client = NotebookClient(nb)
    try:
        client.execute()
    except CellExecutionError as e:
        # Remove colors and other escape characters to make it easier to read in the logs.
        #   https://stackoverflow.com/a/33925425
        error = re.sub(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", "", str(e))

    if error:
        raise RuntimeError(
            f"Error on {repr(ipynb_file)}, section {repr(section)}: {error}"
        )


def run_notebook_parallel(
    ipynb_file: str,
    sections: dict[str, dict],
    prelude: str = "",
    variables: dict = {},
    replace: dict[str, str] = {},
    skip_shell_commands: bool = False,
) -> None:
    args = [
        {
            "ipynb_file": ipynb_file,
            "section": section,
            "prelude": params.get("prelude", prelude),
            "variables": {**variables, **params.get("variables", {})},
            "replace": {**replace, **params.get("replace", {})},
            "skip_shell_commands": params.get(
                "skip_shell_commands", skip_shell_commands
            ),
        }
        for section, params in sections.items()
    ]
    with multiprocessing.Pool(len(args)) as pool:
        pool.map(_run_notebook_section, args)


def _run_notebook_section(kwargs: dict):
    # Helper function to make it pickleable and run with multiprpcessing.
    run_notebook(**kwargs)
