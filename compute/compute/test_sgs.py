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
