#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from argparse import Namespace
import glob
from pathlib import Path
import tempfile

import pytest

from . import sgs

FIXTURE_INGREDIENTS = Path("sgs_test_fixtures/ingredients")
FIXTURE_RECIPES = Path("sgs_test_fixtures/recipes")
FIXTURE_OUTPUT = Path("sgs_test_fixtures/output")


def test_sgs_generate():
    with tempfile.TemporaryDirectory() as tmp_dir:
        args = Namespace(output_dir=tmp_dir)
        sgs.generate(args, FIXTURE_INGREDIENTS.absolute(), FIXTURE_RECIPES.absolute())
        for test_file in map(Path, glob.glob(f"{tmp_dir}/**")):
            match_file = FIXTURE_OUTPUT / test_file.relative_to(tmp_dir)
            assert test_file.read_bytes() == match_file.read_bytes()


def test_snippets_freshness():
    """
    Make sure that the snippets/ folder is up-to-date and matches
    ingredients/ and recipes/. This test will generate SGS output
    in a temporary directory and compare it to the content of
    snippets/ folder.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        args = Namespace(output_dir=tmp_dir)
        sgs.generate(args, Path("ingredients/").absolute(), Path("recipes/").absolute())
        print(list(map(Path, glob.glob(f"{tmp_dir}/**"))))
        for test_file in map(Path, glob.glob(f"{tmp_dir}/**", recursive=True)):
            match_file = Path("snippets/") / test_file.relative_to(tmp_dir)
            if test_file.is_file():
                if test_file.read_bytes() != match_file.read_bytes():
                    pytest.fail(
                        f"This test fails because file {match_file} seems to be outdated. Please run "
                        f"`python sgs.py generate` to update your snippets."
                    )
            elif test_file.is_dir():
                assert match_file.is_dir()
