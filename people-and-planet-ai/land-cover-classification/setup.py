from setuptools import setup, find_packages

setup(
    name="ppai-landcover-classification",
    url="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/people-and-planet-ai/land-cover-classification",
    packages=find_packages(),
    install_requires=[
        "apache-beam[gcp]==2.37.0",
        "earthengine-api==0.1.305",
        "google-cloud-aiplatform==1.12.0",
        "python-snappy==0.6.1",
        "tensorflow==2.8.0",
    ],
)
