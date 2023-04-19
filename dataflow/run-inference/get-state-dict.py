# Copyright 2023 Google LLC
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
import subprocess

import torch
import tempfile
from transformers import T5ForConditionalGeneration

DEFAULT_MODEL = "google/flan-t5-small"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-cache-path", required=True)
    parser.add_argument("--model-name", default=DEFAULT_MODEL)
    args, beam_args = parser.parse_known_args()

    model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    filename = os.path.join(args.model_cache_path, args.model_name, "state_dict.pt")

    if filename.startswith("gs://"):
        with tempfile.NamedTemporaryFile("wb") as f:
            torch.save(model.state_dict(), f.name)
            subprocess.run(["gcloud", "storage", "cp", f.name, filename])
    else:
        torch.save(model.state_dict(), filename)
