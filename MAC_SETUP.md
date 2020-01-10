# Setting up a Mac development environment with pyenv and pyenv-virtualenv

In this guide, you'll set up a local Python development environment with
multiple Python versions, managed by [pyenv](https://github.com/pyenv/pyenv).

This guide differs from the [Google Cloud Python development
instructions](https://cloud.google.com/python/setup) because developers of
samples and libraries need to be able to use multiple versions of Python to
test their code.

## Before you begin

1. Install [homebrew](https://brew.sh/) if you do not already have it.

   **Note:** If you are running Catalina (MacOS 10.15.x), ensure that you have a
   compatible version of Homebrew (2.1.13 or later). Running `brew update` on
   Catalina does not always result in a compatible version, so uninstall and
   reinstall homebrew, if necessary.

## Installing pyenv and pyenv-virtualenv

1.  Install [pyenv](https://github.com/pyenv/pyenv).

    ```console
    brew update
    brew install pyenv
    ```

1.  Install the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
    plugin.

    ```console
    brew install pyenv-virtualenv
    ```

1.  Append the following to your `~/.bashrc`:

    ```
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```

    **Note:** This also works with ZSH.

1.  Reload your shell.

    ```console
    source ~/.bashrc
    ```

## Installing multiple Python versions


1.  See the available Python versions with [pyenv](https://github.com/pyenv/pyenv).

    ```console
    pyenv install --list
    ```

    **Note:** The Python versions are at the top of the long list. If the Python
    version you want isn't listed, you may need to upgrade your pyenv with
    homebrew.

    ```console
    brew update
    brew upgrade pyenv
    ```
    
1.  Install the necessary Python versions with pyenv. Use the latest release
    of the versions you wish to test against.  A list of available versions
    is available on [python.org](https://www.python.org/doc/versions/)

    As of January 8, 2020, the latest Python versions are:

    *  2.7.17 (latest 2.7.x release)
    ```console
    $ pyenv install 2.7.17
    ```
    *  3.5.9 (latest 3.5.x release)
    ```console
    $ pyenv install 3.5.9
    ```
    *  3.6.10 (latest 3.6.x release)
    ```console
    $ pyenv install 3.6.10
    ```
    *  3.7.6 (latest 3.7.x release)
    ```console
    $ pyenv install 3.7.6
    ```
    *  3.8.1 (latest 3.8.x release)
    ```console
    $ pyenv install 3.8.1
    ```

1.  After you have installed a python version through pyenv,
    verify that you are now using the pyenv Python shim.

    ```console
    $ which python
    ~/.pyenv/shims/python
    ```

## Managing python versions using Pyenv global
Pyenv allows you to configure the priority order for your python installs.

```
pyenv global 3.8.1 3.7.6 3.6.10 3.5.9 2.7.17
```

This will make python and python3 point to Python 3.8.1. python2 will use 2.7.17. You can also further specify versions, such as python3.6 to use that version.

## Python virtual environments
Using [Virtual Environments](https://docs.python.org/3/library/venv.html) prevents inadvertent modifications to your global python install. Once created and sourced, calls to `python` will uses this virtual environment, not a global python install. Each virtual environment can have its own set of packages that can be different from others.

To create a virtual environment, run `python3 -m venv`.

```
cd python-docs-samples
python3 -m venv venv-name
source venv-name/bin/activate
```

Typically you will name the venv `venv`, or `venv38` for a python 3.8 venv.

## Nox
The tests for this repository use [nox](https://github.com/theacodes/nox) for managing test runs across multiple python versions. 

```
# List available test runs
nox -l

# Run Firestore cloud client tests using Python 3.6
nox -s "py36(sample='./firestore/cloud-client')"
```

nox creates virtual environments for each of these runs and places them under `.nox/`. For instance you could use the pytest from that test run by calling `.nox/py36-sample-firestore-cloud-client/bin/pytest`
