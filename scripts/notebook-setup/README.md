# Notebook Setup Helper (`notebook_setup.py`)

`notebook_setup.py` provides a standard-library bootstrap utility for notebooks in `python-docs-samples` that depend on sibling Python modules and `requirements.txt` files when opened standalone in Google Colab or Colab Enterprise.

## Usage in a Notebook

```python
# @title Download sample files and install packages (~30 seconds)
from pathlib import Path
import sys
import tempfile
import urllib.request

BRANCH = "main"
SETUP_PATH = Path(tempfile.gettempdir()) / "notebook_setup.py"
for parent in (Path.cwd(), *Path.cwd().parents):
    candidate = parent / "scripts/notebook-setup/notebook_setup.py"
    if candidate.is_file():
        SETUP_PATH = candidate
        break
else:
    if not SETUP_PATH.is_file():
        url = (
            "https://raw.githubusercontent.com/GoogleCloudPlatform/"
            f"python-docs-samples/{BRANCH}/scripts/notebook-setup/notebook_setup.py"
        )
        with urllib.request.urlopen(url, timeout=30) as response:
            SETUP_PATH.write_bytes(response.read())

setup_dir = str(SETUP_PATH.parent.resolve())
if setup_dir not in sys.path:
    sys.path.insert(0, setup_dir)
import notebook_setup

notebook_setup.bootstrap("people-and-planet-ai/weather-forecasting", branch=BRANCH)
```
