from setuptools import find_packages, setup

REQUIRED_PACKAGES = ['tensorflow_datasets~=4.2.0']

setup(
    name='hello-custom-training',
    version='3.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description='Training application for the "Hello custom training" tutorial.'
)
