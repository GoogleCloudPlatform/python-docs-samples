#!/usr/bin/env python
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

from nbconvert.preprocessors import Preprocessor
from typing import Dict
from . import UpdateNotebookVariables as update_notebook_variables


class RemoveNoExecuteCells(Preprocessor):
    def preprocess(self, notebook, resources=None):
        executable_cells = []
        for cell in notebook.cells:
            if cell.metadata.get("tags"):
                if "no_execute" in cell.metadata.get("tags"):
                    continue
            executable_cells.append(cell)
        notebook.cells = executable_cells
        return notebook, resources


class UpdateVariablesPreprocessor(Preprocessor):
    def __init__(self, replacement_map: Dict):
        self._replacement_map = replacement_map

    @staticmethod
    def update_variables(content: str, replacement_map: Dict[str, str]):
        # replace variables inside .ipynb files
        # looking for this format inside notebooks:
        # VARIABLE_NAME = '[description]'

        for variable_name, variable_value in replacement_map.items():
            content = update_notebook_variables.get_updated_value(
                content=content,
                variable_name=variable_name,
                variable_value=variable_value,
            )

        return content

    def preprocess(self, notebook, resources=None):
        executable_cells = []
        for cell in notebook.cells:
            if cell.cell_type == "code":
                cell.source = self.update_variables(
                    content=cell.source,
                    replacement_map=self._replacement_map,
                )

            executable_cells.append(cell)
        notebook.cells = executable_cells
        return notebook, resources
