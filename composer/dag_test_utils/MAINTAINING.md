# Maintenance Guide

## How to release a new version
* Make relevant code changes
* Increment the version number in [setup.py](./setup.py) following [semver](https://semver.org/)
* Add changes to the [CHANGELOG](./CHANGELOG.md)
* If any usage info has changed, update the [README](./README.md)
* [Test the distribution locally](#how-to-test-the-distribution-locally) in the [workflows directory](../workflows)
* Open a PR and request reviews from a [Python Samples owner](https://github.com/orgs/GoogleCloudPlatform/teams/python-samples-owners) and a [Composer Codeowner](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/.github/CODEOWNERS#L24)
* Once the PR is approved and merged, [push the new version to PyPI](#how-to-push-the-new-version-to-pypi)

## How to test the distribution locally
* In a `virtualenv`, run `pip install build`
* Run `python -m build` to build the package. It will create a `dist/` directory containg a wheel (`.whl`) and a tar (`.tar.gz`). 
* Change the [`requirements-test.txt`](../workflows/requirements-test.txt) file in the [`workflows`](../workflows) directory to import your distribution relatively, ensuring that `x.y.z` is replaced with your version number

```
../dag_test_utils/dist/cloud_composer_dag_test_utils-x.y.z.tar.gz
```

* Run `nox -s py-3.8 -- quickstart_test.py` (or the entire nox session, if you prefer) - if it passes without an `ImportError`, congrats! You've done it! 


## How to push the new version to PyPI
Note - these instructions are derived from [the official guide](https://packaging.python.org/tutorials/packaging-projects/) - if they seem to be out of date, please contact `cloud-dpes-composer@`. 

You may only do this after you have successfully tested the package locally and had your PR approved and merged to the primary branch of `python-docs-samples`.

You will need access to the `cloud-dpes-composer` PyPI account and will need an API token. Reach out to `cloud-dpes-composer@` for access. 

* In a `virtualenv`, run `pip install build`
* Run `python -m build` to build the package. It will create a `dist/` directory containg a wheel (`.whl`) and a tar (`.tar.gz`). 
* Run `pip install twine`
* Run `python -m twine upload --repository pypi dist/*`
* For username, put `__token__`. For password, put your API token.
* Voila! Your new version is fully released!


