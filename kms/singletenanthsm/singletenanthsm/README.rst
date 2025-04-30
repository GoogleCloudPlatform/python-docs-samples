Google Cloud Key Management Service Python Samples
===============================================================================

.. image:: https://gstatic.com/cloudssh/images/open-btn.png
   :target: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=kms/singletenanthsm/README.rst


This directory contains samples for Google Cloud Key Management Service. The `Cloud Key Management Service`_ allows you to create, import, and manage cryptographic keys and perform cryptographic operations in a single centralized cloud service.




.. _Cloud Key Management Service: https://cloud.google.com/kms/docs/





Setup
-------------------------------------------------------------------------------


Install Dependencies
++++++++++++++++++++

#. Clone python-kms and change directory to the sample directory you want to use.

    .. code-block:: bash

        $ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

#. Install `pip`_ and `virtualenv`_ if you do not already have them. You may want to refer to the `Python Development Environment Setup Guide`_ for Google Cloud Platform for instructions.

   .. _Python Development Environment Setup Guide:
       https://cloud.google.com/python/setup

#. Create a virtualenv. Samples are compatible with Python 2.7 and 3.4+.

    .. code-block:: bash

        $ virtualenv env
        $ source env/bin/activate

#. Install the dependencies needed to run the samples.

    .. code-block:: bash

        $ pip install -r requirements.txt

.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/

Samples
-------------------------------------------------------------------------------
Create a custom gcloud build to access the Single Tenant HSM service. 

Approve a Single Tenant HSM Instance Proposal. 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Creates custom gcloud build to access single tenant HSM service+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


To run this sample:

.. code-block:: bash

    $ python3 setup.py

    usage: setup.py [-h] [--operation]

    This application creates a custom gcloud build to access the single tenant HSM service.

    positional arguments:
      operation  The type of setup operation you want to perform. This  includes build_custom_gcloud','generate_rsa_keys','generate_gcloud_and_keys'.

    optional arguments:
      -h, --help        show this help message and exit



Approves a Single Tenant HSM Instance Proposal. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
To run this sample:

.. code-block:: bash

    $ python3 approve_proposal.py

    usage: approve_proposal.py [-h] [--proposal_resource PROPOSAL_RESOURCE]

    This application fetches and approves the single tenant HSM instance proposal 
    specified in the "proposal_resource" field.
    
    For more information, visit https://cloud.google.com/kms/docs/attest-key.

    positional arguments:
        --proposal_resource PROPOSAL_RESOURCE
                        The full name of the single tenant HSM instance proposal that needs to be approved.



    optional arguments:
        -h, --help            show this help message and exit


.. _Google Cloud SDK: https://cloud.google.com/sdk/