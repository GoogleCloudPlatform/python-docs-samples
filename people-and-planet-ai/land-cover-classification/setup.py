from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="landcover",
    packages=find_packages(),
    install_requires=requirements,
)
