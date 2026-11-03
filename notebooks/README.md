# Workbench Instances and Notebooks

**Workbench instances** provide a managed, integrated, and secure JupyterLab environment for data scientists, machine learning developers, and agent builders to experiment, develop, and deploy workloads on Google Cloud.

This directory contains Python client library code samples and Jupyter notebook tutorials:
- [Notebooks API v2 code samples](v2)
- [Jupyter notebook tutorials](tutorials)

## Notebooks API v2 (`notebooks/v2`)

In the [v2](v2) folder, you will find atomic Python code samples using the `google-cloud-notebooks` (`google.cloud.notebooks_v2`) client library to create, manage, configure, upgrade, and diagnose Workbench instances.

## Tutorials (`notebooks/tutorials`)

### Run in a Workbench Instance

1. Create a Workbench instance using the Google Cloud console, the `gcloud workbench instances create` CLI command, or the [create_instance.py](v2/create_instance.py) sample.
2. Clone this repository via the JupyterLab terminal or using the Git clone button:

```bash
git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
```

3. Open the `notebooks/tutorials` folder and launch the Jupyter notebooks.

### Run Locally

1. Install JupyterLab or Jupyter Notebook ([installation instructions](https://jupyter.org/install)).
2. Install the dependencies in the [requirements.txt](./requirements.txt) file ([instructions below](#install-the-dependencies)).
3. Register the `google-cloud-bigquery` magic commands ([instructions below](#register-magics-and-configure-matplotlib)).
4. Set `matplotlib` to render inline ([instructions below](#register-magics-and-configure-matplotlib)).

#### Install the dependencies

Install the dependencies with the following command:

```bash
pip install --upgrade -r requirements.txt
```

#### Register magics and configure matplotlib

You can either perform these setup steps in a single notebook, or add the steps to your IPython configuration file to apply to all notebooks.

##### Perform setup steps within a notebook

Run the following commands in your notebook to register the BigQuery magic commands and set `matplotlib` to render inline:

```python
%load_ext google.cloud.bigquery
%matplotlib inline
```

##### Perform setup steps in your IPython configuration file

Add the following code to your `ipython_config.py` file to register the BigQuery magic commands and set `matplotlib` to render inline across all notebooks:

```python
c = get_config()

# Register magic commands
c.InteractiveShellApp.extensions = [
    "google.cloud.bigquery",
]

# Enable matplotlib renderings to render inline in the notebook.
c.InteractiveShellApp.matplotlib = "inline"
```

See the [IPython configuration documentation](https://ipython.readthedocs.io/en/stable/config/intro.html) for more information.
