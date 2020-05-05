# AI Platform Notebooks

[AI Platform Notebooks](https://cloud.google.com/ai-platform-notebooks)
is a managed service that offers an integrated and secure JupyterLab
environment for data scientists and machine learning developers to
experiment, develop, and deploy models into production.

This directory contains AI Platform Notebooks code samples and
tutorials. The tutorials are divided into 2 sections:
- AI Platform Notebooks [API code samples](samples)
- AI Platform Notebooks [tutorials](tutorials)

## Notebooks API

In [this](samples) folder you will find Python code samples to interact
with the
[AI Platform Notebooks API](https://cloud.google.com/ai-platform/notebooks/docs/reference/rest)

## AI Platform Notebooks tutorials

**Run in AI Platform Notebooks**

1. Create a Notebook
   [instance](https://cloud.google.com/ai-platform/notebooks/docs#how-to)
2. Clone this repository via Jupyter console or using the Git clone
   button

```bash
git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
```

3. Open the tutorials folder and open the Jupyter notebooks


**Run locally**

1. Install Jupyter notebooks
   ([instructions](https://jupyter.org/install))
1. Install the dependencies in the [requirements.txt](./requirements.txt) file ([instructions below](#install-the-dependencies))
1. Registered the `google-cloud-bigquery` magic commands ([instructions below](#register-magics-and-configure-matplotlib))
1. Set `matplotlib` to render inline ([instructions below](#register-magics-and-configure-matplotlib))

### Install the dependencies

Install the dependencies with the following command:

        pip install --upgrade -r requirements.txt

### Register magics and configure matplotlib

You can either perform these set up steps in a single notebook, or add the
steps to your IPython configuration file to apply to all notebooks.

### Perform set up steps within a notebook

To perform the set up steps for a single notebook, run the following commands
in your notebook to register the BigQuery magic commands and set `matplotlib`
to render inline:
```python
%load_ext google.cloud.bigquery
%matplotlib inline
```

### Perform set up steps in your IPython configuration file

To perform the set up steps implicitly for all of your notebooks, add the
following code to your `ipython_config.py` file to register the BigQuery magic
commands and set `matplotlib` to render inline:
```python
c = get_config()

# Register magic commands
c.InteractiveShellApp.extensions = [
    'google.cloud.bigquery',
]

# Enable matplotlib renderings to render inline in the notebook.
c.InteractiveShellApp.matplotlib = 'inline'
```
See
[IPython documentation](https://ipython.readthedocs.io/en/stable/config/intro.html)
for more information about IPython configuration.
