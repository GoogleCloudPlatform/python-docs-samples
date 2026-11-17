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

"""Unit tests for the reusable notebook_setup helper."""

from __future__ import annotations

from collections.abc import Callable, Mapping
import importlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import types
from types import ModuleType
from unittest import mock

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "notebook_setup",
    Path(__file__).resolve().parents[1] / "notebook_setup.py",
)
assert _SPEC is not None and _SPEC.loader is not None
notebook_setup = importlib.util.module_from_spec(_SPEC)
sys.modules["notebook_setup"] = notebook_setup
_SPEC.loader.exec_module(notebook_setup)

SAMPLE_SUBPATH = "people-and-planet-ai/weather-forecasting"


def _make_fake_git_runner(
    on_checkout: Callable[[Path], None] | None = None,
) -> Callable[..., subprocess.CompletedProcess[str]]:
    """Builds a `subprocess.run` fake that materializes sparse git directories."""

    def _fake_run(
        cmd: list[str],
        *,
        check: bool = False,
        capture_output: bool = False,
        text: bool = False,
        timeout: float | None = None,
        env: Mapping[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        assert check is True
        assert capture_output is True
        assert text is True
        assert timeout is not None
        assert env is not None and env.get("GIT_TERMINAL_PROMPT") == "0"
        if cmd[:2] == ["git", "clone"]:
            repo_root = Path(cmd[-1])
            (repo_root / ".git").mkdir(parents=True, exist_ok=True)
        elif "checkout" in cmd and ("HEAD" in cmd or "FETCH_HEAD" in cmd):
            repo_root = Path(cmd[2])
            sample_dir = repo_root / SAMPLE_SUBPATH
            sample_dir.mkdir(parents=True, exist_ok=True)
            if on_checkout is not None:
                on_checkout(sample_dir)
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    return _fake_run


def test_bootstrap_fresh_colab_sparse_checkout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "path", list(sys.path))

    def populate_files(sample_dir: Path) -> None:
        (sample_dir / "requirements.txt").write_text(
            "pytest>=8.0.0\n", encoding="utf-8"
        )
        (sample_dir / "visualize.py").write_text("VALUE = 1\n", encoding="utf-8")

    with mock.patch.object(
        notebook_setup.subprocess,
        "run",
        side_effect=_make_fake_git_runner(populate_files),
        autospec=True,
    ) as mock_run:
        resolved = notebook_setup.bootstrap(
            SAMPLE_SUBPATH,
            branch="feat/test-branch",
        )

    expected_repo = tmp_path / "samples-weather-forecasting"
    expected_sample_dir = expected_repo / SAMPLE_SUBPATH
    assert resolved == expected_sample_dir
    assert Path.cwd() == expected_sample_dir
    assert sys.path[0] == str(expected_sample_dir)
    assert (expected_repo / ".git" / "notebook_setup_managed").is_file()

    # 3 git commands on cold clone (clone, sparse-checkout, checkout HEAD) + 1 pip
    cmds = [call.args[0] for call in mock_run.call_args_list]
    assert len(cmds) == 4, f"got {len(cmds)} commands ({cmds!r}), want 4"
    assert "feat/test-branch" in cmds[0]
    assert "--" in cmds[0]
    assert cmds[1][-2:] == ["--", SAMPLE_SUBPATH]
    assert cmds[2][-2:] == ["-f", "HEAD"]
    assert all("fetch" not in cmd for cmd in cmds)
    assert cmds[3][:4] == [sys.executable, "-m", "pip", "install"]
    assert "--upgrade" not in cmds[3]


def test_bootstrap_heals_broken_non_git_cache_and_isolates_reloads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "path", list(sys.path))

    broken_dir = tmp_path / "samples-weather-forecasting"
    broken_dir.mkdir()
    stale_file = broken_dir / "orphan.txt"
    stale_file.write_text("partial", encoding="utf-8")

    expected_sample_dir = broken_dir / SAMPLE_SUBPATH
    fake_mod = ModuleType("visualize")
    fake_mod.__file__ = str(expected_sample_dir / "visualize.py")
    monkeypatch.setitem(sys.modules, "visualize", fake_mod)
    monkeypatch.setitem(sys.modules, "disabled_mod", None)
    assert sys.modules.get("types") is types

    def populate_files(sample_dir: Path) -> None:
        assert not stale_file.exists()
        (sample_dir / "visualize.py").write_text("VALUE = 2\n", encoding="utf-8")
        (sample_dir / "disabled_mod.py").write_text("VALUE = 3\n", encoding="utf-8")
        # Collides by stem with Python stdlib `types`, which must NOT be reloaded.
        (sample_dir / "types.py").write_text("SHADOW = True\n", encoding="utf-8")
        (sample_dir / "visualize_test.py").write_text("TEST = True\n", encoding="utf-8")

    with (
        mock.patch.object(
            notebook_setup.subprocess,
            "run",
            side_effect=_make_fake_git_runner(populate_files),
            autospec=True,
        ),
        mock.patch.object(importlib, "reload", autospec=True) as mock_reload,
    ):
        notebook_setup.bootstrap(SAMPLE_SUBPATH, install_requirements=False)

    mock_reload.assert_called_once_with(fake_mod)


def test_bootstrap_unlinks_conflicting_file_or_symlink_at_repo_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "path", list(sys.path))

    target_dir = tmp_path / "external-target"
    target_dir.mkdir()
    keep_file = target_dir / "keep.txt"
    keep_file.write_text("must survive\n", encoding="utf-8")

    symlink_root = tmp_path / "samples-weather-forecasting"
    symlink_root.symlink_to(target_dir, target_is_directory=True)

    with mock.patch.object(
        notebook_setup.subprocess,
        "run",
        side_effect=_make_fake_git_runner(),
        autospec=True,
    ):
        resolved = notebook_setup.bootstrap(SAMPLE_SUBPATH, install_requirements=False)

    assert resolved.is_dir()
    assert keep_file.read_text(encoding="utf-8") == "must survive\n"


def test_bootstrap_updates_when_already_inside_managed_clone(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "samples-weather-forecasting"
    (repo_root / ".git").mkdir(parents=True)
    (repo_root / ".git" / "notebook_setup_managed").write_text(
        "managed\n", encoding="utf-8"
    )
    sample_dir = repo_root / SAMPLE_SUBPATH
    sample_dir.mkdir(parents=True)
    monkeypatch.chdir(sample_dir)
    monkeypatch.setattr(sys, "path", ["/other/path", str(sample_dir)])

    with mock.patch.object(
        notebook_setup.subprocess,
        "run",
        return_value=subprocess.CompletedProcess(["git"], 0, stdout="", stderr=""),
        autospec=True,
    ) as mock_run:
        resolved = notebook_setup.bootstrap(
            SAMPLE_SUBPATH,
            branch="main",
            install_requirements=False,
        )

    assert resolved == sample_dir
    assert sys.path[0] == str(sample_dir)
    # Warm clone runs sparse-checkout, fetch, and checkout FETCH_HEAD (no clone)
    cmds = [call.args[0] for call in mock_run.call_args_list]
    assert len(cmds) == 3, f"got {len(cmds)} commands ({cmds!r}), want 3"
    assert "sparse-checkout" in cmds[0]
    assert "fetch" in cmds[1] and "main" in cmds[1]
    assert cmds[2][-2:] == ["-f", "FETCH_HEAD"]


def test_bootstrap_preserves_local_developer_checkout_without_git_reset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local_repo = tmp_path / "python-docs-samples"
    (local_repo / ".git").mkdir(parents=True)
    sample_dir = local_repo / SAMPLE_SUBPATH
    sample_dir.mkdir(parents=True)
    local_edit = sample_dir / "uncommitted.py"
    local_edit.write_text("LOCAL = True\n", encoding="utf-8")

    monkeypatch.chdir(local_repo)
    monkeypatch.setattr(sys, "path", list(sys.path))

    with mock.patch.object(notebook_setup.subprocess, "run", autospec=True) as mock_run:
        resolved = notebook_setup.bootstrap(
            SAMPLE_SUBPATH,
            install_requirements=False,
        )

    assert resolved == sample_dir
    assert Path.cwd() == sample_dir
    assert local_edit.read_text(encoding="utf-8") == "LOCAL = True\n"
    mock_run.assert_not_called()


def test_bootstrap_refuses_unmanaged_git_repo_at_clone_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unmanaged_repo = tmp_path / "python-docs-samples"
    (unmanaged_repo / ".git").mkdir(parents=True)
    monkeypatch.chdir(tmp_path)

    with (
        mock.patch.object(notebook_setup.subprocess, "run", autospec=True) as mock_run,
        pytest.raises(RuntimeError, match="unmanaged git repository"),
    ):
        notebook_setup.bootstrap(
            SAMPLE_SUBPATH,
            clone_dir="python-docs-samples",
            install_requirements=False,
        )

    mock_run.assert_not_called()


def test_bootstrap_raises_file_not_found_for_missing_sample_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local_repo = tmp_path / "python-docs-samples"
    (local_repo / ".git").mkdir(parents=True)
    monkeypatch.chdir(local_repo)

    with pytest.raises(FileNotFoundError, match="not found"):
        notebook_setup.bootstrap("nonexistent/sample", install_requirements=False)


def test_bootstrap_surfaces_subprocess_stderr_on_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    err = subprocess.CalledProcessError(
        128,
        ["git", "clone"],
        output="",
        stderr="fatal: Remote branch missing-branch not found in upstream origin\n",
    )
    with (
        mock.patch.object(
            notebook_setup.subprocess, "run", side_effect=err, autospec=True
        ),
        pytest.raises(RuntimeError, match="Remote branch missing-branch not found"),
    ):
        notebook_setup.bootstrap(SAMPLE_SUBPATH, branch="missing-branch")


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"sample_subpath": "   /  "}, "non-empty"),
        ({"sample_subpath": "foo/../../outside"}, "relative path"),
        ({"sample_subpath": "-upload-pack=bad"}, "leading '-'"),
        ({"sample_subpath": SAMPLE_SUBPATH, "clone_dir": "."}, "single relative"),
        ({"sample_subpath": SAMPLE_SUBPATH, "clone_dir": "../sibling"}, "single"),
        ({"sample_subpath": SAMPLE_SUBPATH, "branch": "--upload-pack=x"}, "branch"),
        ({"sample_subpath": SAMPLE_SUBPATH, "repo_url": "--upload-pack=x"}, "repo_url"),
    ],
)
def test_bootstrap_rejects_unsafe_inputs(
    kwargs: dict[str, str],
    match: str,
) -> None:
    with pytest.raises(ValueError, match=match):
        notebook_setup.bootstrap(**kwargs)
