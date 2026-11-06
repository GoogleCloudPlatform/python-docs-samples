# Copyright 2026 Google LLC
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

"""Reusable sparse-checkout and package setup helper for sample notebooks."""

from __future__ import annotations

from collections.abc import Sequence
import importlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

DEFAULT_REPO_URL = "https://github.com/GoogleCloudPlatform/python-docs-samples.git"
_MANAGED_MARKER = "notebook_setup_managed"


def _find_git_root(start: Path) -> Path | None:
    """Walks upward from `start` to find an enclosing `.git` directory."""
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _is_managed_clone(repo_root: Path) -> bool:
    """Returns True if `repo_root` was created and managed by `notebook_setup`."""
    return (repo_root / ".git" / _MANAGED_MARKER).is_file()


def _reload_sample_modules(
    sample_dir: Path,
    extra_modules: Sequence[str] = (),
) -> None:
    """Reloads already-imported sibling Python modules in `sample_dir`."""
    importlib.invalidate_caches()
    local_stems = {
        py_file.stem
        for py_file in sample_dir.glob("*.py")
        if py_file.stem != "__init__" and not py_file.stem.startswith("test_")
    }
    local_stems.update(extra_modules)
    for mod_name in sorted(local_stems):
        module = sys.modules.get(mod_name)
        if module is not None:
            importlib.reload(module)


def bootstrap(
    sample_subpath: str,
    *,
    branch: str = "main",
    repo_url: str = DEFAULT_REPO_URL,
    clone_dir: str | None = None,
    install_requirements: bool = True,
    reload_modules: Sequence[str] = (),
) -> Path:
    """Sparse-clones or updates `sample_subpath` and installs its dependencies.

    When executed inside an existing local developer or CI checkout of the
    repository, `bootstrap` leaves local working-tree files untouched (no
    `git fetch` or `git checkout -f`), switches into `sample_subpath`, updates
    `sys.path`, and optionally installs `requirements.txt`.

    When executed in an ephemeral or persistent notebook environment (such as
    Google Colab or Colab Enterprise) where only the `.ipynb` file was imported,
    `bootstrap` creates or updates a managed sparse checkout, self-heals
    interrupted partial directories, checks out the latest `FETCH_HEAD` for
    `branch`, installs `requirements.txt`, and reloads any previously imported
    sibling sample modules.

    Args:
        sample_subpath: Repository-relative path to the sample directory (for
            example, `'people-and-planet-ai/weather-forecasting'`).
        branch: Git branch or tag to fetch when managing a notebook clone.
        repo_url: Git remote URL to sparse-clone when not in a local checkout.
        clone_dir: Optional directory name for the managed sparse clone.
            Defaults to `'samples-<sample-leaf-name>'`.
        install_requirements: Whether to install `requirements.txt` with `pip`.
        reload_modules: Optional extra module names to reload if already in
            `sys.modules`.

    Returns:
        Resolved `Path` to the active sample directory.
    """
    normalized_subpath = sample_subpath.strip().strip("/")
    if not normalized_subpath or normalized_subpath in {".", ".."}:
        raise ValueError("sample_subpath must be a non-empty relative path.")

    cwd = Path.cwd().resolve()
    enclosing_git_root = _find_git_root(cwd)

    if enclosing_git_root is not None and not _is_managed_clone(enclosing_git_root):
        sample_dir = (enclosing_git_root / normalized_subpath).resolve()
        if not sample_dir.is_dir():
            raise FileNotFoundError(
                f"Sample directory '{normalized_subpath}' not found inside "
                f"local repository '{enclosing_git_root}'."
            )
    else:
        if enclosing_git_root is not None and _is_managed_clone(enclosing_git_root):
            repo_root = enclosing_git_root
        else:
            leaf_name = Path(normalized_subpath).name
            target_dir_name = clone_dir or f"samples-{leaf_name}"
            repo_root = (cwd / target_dir_name).resolve()

        if repo_root.exists() and not (repo_root / ".git").exists():
            if repo_root.is_dir():
                shutil.rmtree(repo_root)
            else:
                repo_root.unlink()

        if not repo_root.exists():
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--filter=blob:none",
                    "--no-checkout",
                    "--depth",
                    "1",
                    "--sparse",
                    "-b",
                    branch,
                    repo_url,
                    str(repo_root),
                ],
                check=True,
            )
            (repo_root / ".git" / _MANAGED_MARKER).write_text(
                "managed-by-notebook-setup\n",
                encoding="utf-8",
            )

        subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "sparse-checkout",
                "set",
                normalized_subpath,
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "fetch",
                "--depth",
                "1",
                "origin",
                branch,
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "-c",
                "advice.detachedHead=false",
                "checkout",
                "-f",
                "FETCH_HEAD",
            ],
            check=True,
        )
        sample_dir = (repo_root / normalized_subpath).resolve()

    os.chdir(sample_dir)
    sample_dir_str = str(sample_dir)
    if sample_dir_str not in sys.path:
        sys.path.insert(0, sample_dir_str)

    req_file = sample_dir / "requirements.txt"
    if install_requirements and req_file.is_file():
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                "-r",
                str(req_file),
            ],
            check=True,
        )

    _reload_sample_modules(sample_dir, extra_modules=reload_modules)
    return sample_dir
