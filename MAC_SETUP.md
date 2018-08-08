# Setting up a Mac development environment with pyenv and pyenv-virtualenv

In this guide, you'll set up a local Python development environment with
multiple Python versions, managed by [pyenv](https://github.com/pyenv/pyenv).

## Before you begin

1.  [Optional] Install [homebrew](https://brew.sh/).

## Installing pyenv and pyenv-virtualenv

1.  Install [pyenv](https://github.com/pyenv/pyenv).

    I (tswast@) use [homebrew](https://brew.sh/) to install it.

    ```
    brew update
    brew install pyenv
    ```

1.  Install the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
    plugin.

1.  Add

    ```
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"`
    ```

    to your shell RC file, such as `~/.bashrc`, and reload your shell.

1.  Verify that you are now using the pyenv Python shim.

    ```
    $ which python
    /Users/tswast/.pyenv/shims/python
    ```

## Installing multiple Python versions


1.  See the available Python versions with

    ```
    pyenv install --list
    ```

    The python versions are at the top of the long list.

    If the Python version you want isn't listed, you may need to upgrade
    your pyenv with homebrew.

    ```
    brew update
    brew upgrade pyenv
    ```

1.  Compile the necessary Python versions with pyenv.

    As of August 8, 2018 my (tswast@) Python versions are:

    *  2.7.15
    *  3.5.4
    *  3.6.4
    *  3.7.0

## Using pyenv and pyenv-virtualenv to manage your Python versions

1.  Change to the desired source directory.

    ```
    cd ~/src/python-docs-samples
    ```

1.  Create a virtualenv using `pyenv virtualenv`.

    ```
    pyenv virtualenv 3.6.4 python-docs-samples
    ```

    This creates a virtualenv folder within `~/.pyenv/versions/`.

1.  Set the local Python version(s) with `pyenv local`

    ```
    pyenv local python-docs-samples 3.6.4 3.7.0 3.5.4 2.715
    ```

1.  Now when you `cd` into the source directory or a subdirectory within it,
    pyenv will make your virtualenv the default Python. Since you specified
    more than one version, it will also add binaries like `python36` and
    `python27` to your PATH, which nox uses when picking Python interpreters.

1.  Since we don't want to add the pyenv configuration to git, add
    `.python-version` to your [global gitignore
    file](https://help.github.com/articles/ignoring-files/#create-a-global-gitignore).
