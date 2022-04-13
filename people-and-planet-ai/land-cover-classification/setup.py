from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="ppai-landcover-classification",
    packages=find_packages(),
    install_requires=requirements,
)
