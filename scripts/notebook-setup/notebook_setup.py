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
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys

DEFAULT_REPO_URL = "https://github.com/GoogleCloudPlatform/python-docs-samples.git"
_MANAGED_MARKER = "notebook_setup_managed"
_NETWORK_TIMEOUT_SECONDS = 300.0
_LOCAL_GIT_TIMEOUT_SECONDS = 30.0


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


def _validate_inputs(
    sample_subpath: str,
    branch: str,
    repo_url: str,
    clone_dir: str | None,
) -> tuple[str, str, str]:
    """Validates path and git arguments and returns normalized values."""
    raw_subpath = sample_subpath.strip().strip("/")
    parts = PurePosixPath(raw_subpath).parts
    if (
        not parts
        or "\\" in sample_subpath
        or any(part in {"", ".", ".."} for part in parts)
        or parts[0].startswith("-")
    ):
        raise ValueError(
            f"sample_subpath {sample_subpath!r} must be a non-empty relative path "
            "without '..' segments or leading '-'."
        )

    clean_branch = branch.strip()
    if (
        not clean_branch
        or clean_branch.startswith("-")
        or any(ch.isspace() for ch in clean_branch)
    ):
        raise ValueError(f"Invalid git branch or tag {branch!r}.")

    clean_repo_url = repo_url.strip()
    if (
        not clean_repo_url
        or clean_repo_url.startswith("-")
        or any(ch.isspace() for ch in clean_repo_url)
    ):
        raise ValueError(f"Invalid repo_url {repo_url!r}.")

    if clone_dir is not None:
        raw_clone = clone_dir.strip()
        clone_parts = PurePosixPath(raw_clone).parts
        if (
            len(clone_parts) != 1
            or "\\" in raw_clone
            or raw_clone.startswith("/")
            or clone_parts[0] in {"", ".", ".."}
            or clone_parts[0].startswith("-")
        ):
            raise ValueError(
                f"clone_dir {clone_dir!r} must be a single relative directory name."
            )

    return "/".join(parts), clean_branch, clean_repo_url


def _run_command(cmd: Sequence[str], *, timeout: float) -> None:
    """Executes a subprocess non-interactively and surfaces stderr on failure."""
    env = {
        **os.environ,
        "GIT_TERMINAL_PROMPT": "0",
        "PIP_NO_INPUT": "1",
    }
    cmd_list = list(cmd)
    try:
        subprocess.run(
            cmd_list,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.CalledProcessError as err:
        detail = (err.stderr or err.stdout or "").strip()
        suffix = f": {detail}" if detail else "."
        raise RuntimeError(
            f"Command {cmd_list!r} failed with exit code {err.returncode}{suffix}"
        ) from err


def _sync_managed_clone(
    repo_root: Path,
    normalized_subpath: str,
    branch: str,
    repo_url: str,
) -> Path:
    """Creates or updates a managed sparse checkout and returns `sample_dir`."""
    if (repo_root / ".git").exists() and not _is_managed_clone(repo_root):
        raise RuntimeError(
            f"Refusing to modify existing unmanaged git repository at '{repo_root}'. "
            "Pass a distinct clone_dir or run inside that checkout."
        )

    if repo_root.is_symlink() or (
        repo_root.exists() and not (repo_root / ".git").exists()
    ):
        if not repo_root.is_symlink() and repo_root.is_dir():
            shutil.rmtree(repo_root)
        else:
            repo_root.unlink()

    is_fresh_clone = not repo_root.exists()
    if is_fresh_clone:
        _run_command(
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
                "--",
                repo_url,
                str(repo_root),
            ],
            timeout=_NETWORK_TIMEOUT_SECONDS,
        )
        (repo_root / ".git" / _MANAGED_MARKER).write_text(
            "managed-by-notebook-setup\n",
            encoding="utf-8",
        )

    _run_command(
        [
            "git",
            "-C",
            str(repo_root),
            "sparse-checkout",
            "set",
            "--",
            normalized_subpath,
        ],
        timeout=_LOCAL_GIT_TIMEOUT_SECONDS,
    )
    if is_fresh_clone:
        _run_command(
            [
                "git",
                "-C",
                str(repo_root),
                "-c",
                "advice.detachedHead=false",
                "checkout",
                "-f",
                "HEAD",
            ],
            timeout=_NETWORK_TIMEOUT_SECONDS,
        )
    else:
        _run_command(
            [
                "git",
                "-C",
                str(repo_root),
                "fetch",
                "--depth",
                "1",
                "--",
                "origin",
                branch,
            ],
            timeout=_NETWORK_TIMEOUT_SECONDS,
        )
        _run_command(
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
            timeout=_NETWORK_TIMEOUT_SECONDS,
        )

    sample_dir = (repo_root / normalized_subpath).resolve()
    if not sample_dir.is_relative_to(repo_root) or not sample_dir.is_dir():
        raise FileNotFoundError(
            f"Sample directory '{normalized_subpath}' not found in '{repo_root}' "
            f"(branch '{branch}')."
        )
    return sample_dir


def _is_reloadable_sample_file(py_file: Path) -> bool:
    """Returns True if `py_file` is a sample module rather than test/CI config."""
    stem = py_file.stem
    return (
        stem
        not in {
            "__init__",
            "conftest",
            "notebook_setup",
            "noxfile",
            "noxfile_config",
        }
        and not stem.startswith("test_")
        and not stem.endswith("_test")
    )


def _reload_sample_modules(
    sample_dir: Path,
    extra_modules: Sequence[str] = (),
) -> None:
    """Reloads already-imported sibling Python modules originating in `sample_dir`."""
    importlib.invalidate_caches()
    resolved_dir = sample_dir.resolve()
    explicit = set(extra_modules)
    candidates = {
        py_file.stem
        for py_file in resolved_dir.glob("*.py")
        if _is_reloadable_sample_file(py_file)
    } | explicit
    for mod_name in sorted(candidates):
        module = sys.modules.get(mod_name)
        if module is None:
            continue
        mod_file = getattr(module, "__file__", None)
        if mod_name in explicit or (
            mod_file is not None
            and Path(mod_file).resolve().is_relative_to(resolved_dir)
        ):
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
    interrupted partial directories, checks out the target `branch`, installs
    `requirements.txt`, and reloads any previously imported sibling sample
    modules.

    Args:
        sample_subpath: Repository-relative path to the sample directory (for
            example, `'people-and-planet-ai/weather-forecasting'`).
        branch: Git branch or tag to fetch when managing a notebook clone.
        repo_url: Git remote URL to sparse-clone when not in a local checkout.
        clone_dir: Optional single relative directory name for the managed
            sparse clone. Defaults to `'samples-<sample-leaf-name>'`.
        install_requirements: Whether to install `requirements.txt` with `pip`.
        reload_modules: Optional extra module names to reload if already in
            `sys.modules`.

    Returns:
        Resolved `Path` to the active sample directory.

    Raises:
        ValueError: If `sample_subpath`, `branch`, `repo_url`, or `clone_dir`
            is empty or contains unsafe path/flag segments.
        FileNotFoundError: If `sample_subpath` does not exist in the repository.
        RuntimeError: If `repo_root` is an unmanaged git checkout or if a `git`
            or `pip` command fails.
        subprocess.TimeoutExpired: If a `git` or `pip` subprocess exceeds its
            timeout.
    """
    normalized_subpath, clean_branch, clean_repo_url = _validate_inputs(
        sample_subpath, branch, repo_url, clone_dir
    )

    cwd = Path.cwd().resolve()
    enclosing_git_root = _find_git_root(cwd)

    if enclosing_git_root is not None and not _is_managed_clone(enclosing_git_root):
        sample_dir = (enclosing_git_root / normalized_subpath).resolve()
        if not sample_dir.is_relative_to(enclosing_git_root) or not sample_dir.is_dir():
            raise FileNotFoundError(
                f"Sample directory '{normalized_subpath}' not found inside "
                f"local repository '{enclosing_git_root}'."
            )
    else:
        if enclosing_git_root is not None and _is_managed_clone(enclosing_git_root):
            repo_root = enclosing_git_root
        else:
            leaf_name = PurePosixPath(normalized_subpath).name
            target_dir_name = (
                clone_dir.strip() if clone_dir is not None else f"samples-{leaf_name}"
            )
            repo_root = cwd / target_dir_name

        sample_dir = _sync_managed_clone(
            repo_root=repo_root,
            normalized_subpath=normalized_subpath,
            branch=clean_branch,
            repo_url=clean_repo_url,
        )

    os.chdir(sample_dir)
    sample_dir_str = str(sample_dir)
    if sample_dir_str in sys.path:
        sys.path.remove(sample_dir_str)
    sys.path.insert(0, sample_dir_str)

    req_file = sample_dir / "requirements.txt"
    if install_requirements and req_file.is_file():
        _run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                "-r",
                str(req_file),
            ],
            timeout=_NETWORK_TIMEOUT_SECONDS,
        )

    _reload_sample_modules(sample_dir, extra_modules=reload_modules)
    return sample_dir
