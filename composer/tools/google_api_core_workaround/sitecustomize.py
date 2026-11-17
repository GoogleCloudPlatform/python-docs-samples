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

"""CPython sitecustomize hook for patching google.api_core deprecation check."""

import datetime
import importlib.util
import os
import sys

# Remove this patch directory from sys.path to avoid redundant lookups
# on subsequent module imports when loaded via PYTHONPATH.
_patch_file = globals().get("__file__")
if _patch_file:
    _patch_dir = os.path.abspath(os.path.dirname(_patch_file))
    _is_site_dir = any(
        part in ("site-packages", "dist-packages")
        for part in _patch_dir.split(os.sep)
    )
    if not _is_site_dir:
        _patch_dir_slash = _patch_dir + os.sep
        sys.path[:] = [
            p
            for p in sys.path
            if not isinstance(p, (str, os.PathLike))
            or not os.path.isabs(p)
            or (
                os.path.abspath(p) != _patch_dir
                and os.path.abspath(p) != _patch_dir_slash
            )
        ]
        sys.path_importer_cache.pop(_patch_dir, None)
        sys.path_importer_cache.pop(_patch_dir_slash, None)

TARGET_MODULE = "google.api_core._python_version_support"


class _GoogleApiCorePatcher:
    """Import hook to patch DEPRECATION_WARNING_PERIOD on load."""

    def find_spec(self, fullname, path=None, target=None):
        if fullname == TARGET_MODULE:
            try:
                sys.meta_path.remove(self)
            except ValueError:
                pass

            try:
                spec = importlib.util.find_spec(fullname)
            except Exception:
                return None

            if spec and spec.loader:
                orig_exec_module = spec.loader.exec_module

                def exec_module(module):
                    import importlib.metadata

                    orig_packages_distributions = getattr(
                        importlib.metadata, "packages_distributions", None
                    )
                    if orig_packages_distributions:
                        importlib.metadata.packages_distributions = lambda: {}
                    try:
                        orig_exec_module(module)
                    finally:
                        if orig_packages_distributions:
                            importlib.metadata.packages_distributions = (
                                orig_packages_distributions
                            )
                    module.DEPRECATION_WARNING_PERIOD = datetime.timedelta(days=60)
                    module._get_pypi_package_name = lambda module_name: None

                spec.loader.exec_module = exec_module
            return spec
        return None


if not any(type(h).__name__ == "_GoogleApiCorePatcher" for h in sys.meta_path):
    sys.meta_path.insert(0, _GoogleApiCorePatcher())
