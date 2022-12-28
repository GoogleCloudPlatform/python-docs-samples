# Setting up a Mac development environment with pyenv and pyenv-virtualenv

In this guide, you'll set up a local Python development environment with
multiple Python versions, managed by [pyenv](https://github.com/pyenv/pyenv).

This guide differs from the [Google Cloud Python development
instructions](https://cloud.google.com/python/setup) because developers of
samples and libraries need to be able to use multiple versions of Python to
test their code.

## Before you begin

1. Install [homebrew](https://brew.sh/) if you do not already have it.

   **Note:** If you are running Catalina (MacOS 10.15.x), ensure that you have
   a compatible version of Homebrew (2.1.13 or later). Running `brew update` on
   Catalina does not always result in a compatible version, so uninstall and
   reinstall homebrew, if necessary

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

    As of April 28, 2022, the latest Python versions are:

    *  3.6.13 (latest 3.6.x release)
    ```console
    $ pyenv install 3.6.13
    ```
    *  3.7.13 (latest 3.7.x release)
    ```console
    $ pyenv install 3.7.13
    ```
    *  3.8.13 (latest 3.8.x release)
    ```console
    $ pyenv install 3.8.13
    ```
    *  3.9.12 (latest 3.9.x release)
    ```console
    $ pyenv install 3.9.12
    ```
    *  3.10.4 (latest 3.10.x release)
    ```console
    $ pyenv install 3.10.4
    ```
    
    > ℹ️ *Note*: If you are using an M1 Mac,
    > certain versions of Python will not properly install with pyenv
    > due to [incompatibilities with `clang`](https://bugs.python.org/issue45405).
    > Python 3.6.13, 3.7.13, and 3.8.13 will work, but earlier patches Python 3.6, Python 3.7, and Python 3.8 may not. 


    > ℹ️ *Note*: If you are getting errors installing a python version,
    > try setting up the `SDKROOT` environment variable.
    >
    > ```console
    > # You can add this to your .bashrc file.
    > export SDKROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk
    > ```

1.  After you have installed a python version through pyenv,
    verify that you are now using the pyenv Python shim.

    ```console
    $ which python
    ~/.pyenv/shims/python
    ```

## Managing python versions using Pyenv global
Pyenv allows you to configure the priority order for your python installs.

```
pyenv global 3.8.5 3.7.8 3.6.11 3.5.9 2.7.18
```

This will make python and python3 point to Python 3.8.5. python2 will use
2.7.18. You can also further specify versions, such as python3.6 to use that
version.

## Python virtual environments
Using [Virtual Environments](https://docs.python.org/3/library/venv.html)
prevents inadvertent modifications to your global python install. Once
created and sourced, calls to `python` will use this virtual environment, not
a global python install. Each virtual environment can have its own set of
packages that can be different from others.


### Using Python 3+ venv
Python has builtin support for creating virtual environments, accessible by
running the `venv` module.

```
cd python-docs-samples
python -m venv [venv-name]
source [venv-name]/bin/activate
```

Typically you will name the venv `venv`, or `venv38` for a python 3.8 venv.


### Using pyenv-virtualenv
You can also use an extension for pyenv that will assist in managing virtual
environments. This allows you to use `pyenv local` to automatically use the
created virtual environment. You can install this by running
`$ brew install pyenv-virtualenv`

1.  Change to the desired source directory.	

    ```console	
    cd ~/src/python-docs-samples	
    ```	

1.  Create a virtualenv for python 3.8.5 using `pyenv virtualenv`.	

    ```console	
    pyenv virtualenv 3.8.5 python-docs-samples	
    ```	

    This creates a virtualenv folder within `~/.pyenv/versions/`.	

1.  Set the local Python version(s) with `pyenv local`	

    ```console	
    # pyenv local [name of virtualenv] [list of python versions to use]	
    pyenv local python-docs-samples 3.8.5 3.7.8 3.6.11 3.5.9 2.7.18	
    ```	

1.  Now, when you `cd` into the source directory or a subdirectory within it,	
    pyenv will make your virtualenv the default Python. Since you specified	
    more than one version, it will also add binaries like `python36` and	
    `python27` to your PATH, which
    [nox](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/AUTHORING_GUIDE.md#running-tests-with-nox)
    uses when picking Python interpreters.	

1.  Add `.python-version` to your
    [global gitignore file](https://help.github.com/articles/ignoring-files/#create-a-global-gitignore),	
    so it won't be committed into the repository.

## More on authoring samples
If you are looking for more information on how to author samples, please view
the [Authoring Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/AUTHORING_GUIDE.md)
