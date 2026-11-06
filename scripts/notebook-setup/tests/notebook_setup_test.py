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

import importlib
import importlib.util
from pathlib import Path
import subprocess
import sys
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


def test_bootstrap_fresh_colab_sparse_checkout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "path", list(sys.path))

    def fake_run(
        cmd: list[str],
        *,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        assert check is True
        if cmd[:2] == ["git", "clone"]:
            repo_root = Path(cmd[-1])
            (repo_root / ".git").mkdir(parents=True, exist_ok=True)
        elif "checkout" in cmd and "FETCH_HEAD" in cmd:
            repo_root = Path(cmd[2])
            sample_dir = repo_root / SAMPLE_SUBPATH
            sample_dir.mkdir(parents=True, exist_ok=True)
            (sample_dir / "requirements.txt").write_text(
                "pytest>=8.0.0\n", encoding="utf-8"
            )
            (sample_dir / "visualize.py").write_text("VALUE = 1\n", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0)

    with mock.patch.object(
        notebook_setup.subprocess, "run", side_effect=fake_run, autospec=True
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
    # 4 git commands (clone, sparse-checkout, fetch, checkout) + 1 pip install
    assert mock_run.call_count == 5
    pip_cmd = mock_run.call_args_list[-1].args[0]
    assert pip_cmd[:4] == [sys.executable, "-m", "pip", "install"]
    assert "--upgrade" not in pip_cmd


def test_bootstrap_heals_broken_non_git_cache_and_reloads_module(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "path", list(sys.path))

    broken_dir = tmp_path / "samples-weather-forecasting"
    broken_dir.mkdir()
    stale_file = broken_dir / "orphan.txt"
    stale_file.write_text("partial", encoding="utf-8")

    fake_mod = ModuleType("visualize")
    monkeypatch.setitem(sys.modules, "visualize", fake_mod)
    monkeypatch.setitem(sys.modules, "disabled_mod", None)

    def fake_run(
        cmd: list[str],
        *,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        assert check is True
        if cmd[:2] == ["git", "clone"]:
            assert not stale_file.exists()
            repo_root = Path(cmd[-1])
            (repo_root / ".git").mkdir(parents=True, exist_ok=True)
        elif "checkout" in cmd and "FETCH_HEAD" in cmd:
            repo_root = Path(cmd[2])
            sample_dir = repo_root / SAMPLE_SUBPATH
            sample_dir.mkdir(parents=True, exist_ok=True)
            (sample_dir / "visualize.py").write_text("VALUE = 2\n", encoding="utf-8")
            (sample_dir / "disabled_mod.py").write_text("VALUE = 3\n", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0)

    with (
        mock.patch.object(
            notebook_setup.subprocess, "run", side_effect=fake_run, autospec=True
        ),
        mock.patch.object(importlib, "reload", autospec=True) as mock_reload,
    ):
        notebook_setup.bootstrap(SAMPLE_SUBPATH, install_requirements=False)

    mock_reload.assert_called_once_with(fake_mod)


def test_bootstrap_unlinks_conflicting_file_at_repo_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "path", list(sys.path))

    conflicting_file = tmp_path / "samples-weather-forecasting"
    conflicting_file.write_text("accidental file", encoding="utf-8")

    def fake_run(
        cmd: list[str],
        *,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        assert check is True
        if cmd[:2] == ["git", "clone"]:
            repo_root = Path(cmd[-1])
            assert not repo_root.is_file()
            (repo_root / ".git").mkdir(parents=True, exist_ok=True)
        elif "checkout" in cmd and "FETCH_HEAD" in cmd:
            repo_root = Path(cmd[2])
            (repo_root / SAMPLE_SUBPATH).mkdir(parents=True, exist_ok=True)
        return subprocess.CompletedProcess(cmd, 0)

    with mock.patch.object(
        notebook_setup.subprocess, "run", side_effect=fake_run, autospec=True
    ):
        resolved = notebook_setup.bootstrap(SAMPLE_SUBPATH, install_requirements=False)

    assert resolved.is_dir()


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
    monkeypatch.setattr(sys, "path", list(sys.path))

    with mock.patch.object(notebook_setup.subprocess, "run", autospec=True) as mock_run:
        resolved = notebook_setup.bootstrap(
            SAMPLE_SUBPATH,
            branch="main",
            install_requirements=False,
        )

    assert resolved == sample_dir
    # Should run sparse-checkout, fetch, and checkout (no git clone)
    cmds = [call.args[0] for call in mock_run.call_args_list]
    assert len(cmds) == 3
    assert cmds[0][:2] == ["git", "-C"]
    assert "sparse-checkout" in cmds[0]
    assert "fetch" in cmds[1]
    assert "checkout" in cmds[2]


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


def test_bootstrap_rejects_empty_subpath() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        notebook_setup.bootstrap("   /  ")
