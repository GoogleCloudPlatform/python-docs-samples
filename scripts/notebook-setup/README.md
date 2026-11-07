# Notebook Setup Helper (`notebook_setup.py`)

Reusable standard-library bootstrap utility for notebooks in `python-docs-samples` that depend on sibling Python modules and `requirements.txt` files when opened standalone in Google Colab or Colab Enterprise.

## Usage in a Notebook

```python
# @title Download sample files and install packages (~30 seconds)
from pathlib import Path
import sys
import urllib.request

BRANCH = "main"
SETUP_PATH = Path("notebook_setup.py")
for parent in (Path.cwd(), *Path.cwd().parents):
    candidate = parent / "scripts/notebook-setup/notebook_setup.py"
    if candidate.is_file():
        SETUP_PATH = candidate
        break
else:
    if not SETUP_PATH.is_file():
        urllib.request.urlretrieve(
            f"https://raw.githubusercontent.com/GoogleCloudPlatform/python-docs-samples/{BRANCH}/scripts/notebook-setup/notebook_setup.py",
            SETUP_PATH,
        )

sys.path.insert(0, str(SETUP_PATH.parent.resolve()))
import notebook_setup

notebook_setup.bootstrap("people-and-planet-ai/weather-forecasting", branch=BRANCH)
```
