Authentication
++++++++++++++

Authentication is typically done through `Application Default Credentials`_,
which means you do not have to change the code to authenticate as long as
your environment has credentials. You have a few options for setting up
authentication:

{% if not no_sdk_credentials %}
#. When running locally, use the `Google Cloud SDK`_

    .. code-block:: bash

        gcloud beta auth application-default login

{% endif %}

#. When running on App Engine or Compute Engine, credentials are already
   set-up. However, you may need to configure your Compute Engine instance
   with `additional scopes`_.

#. You can create a `Service Account key file`_. This file can be used to
   authenticate to Google Cloud Platform services from any environment. To use
   the file, set the ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable to
   the path to the key file, for example:

    .. code-block:: bash

        export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json

.. _Application Default Credentials: https://cloud.google.com/docs/authentication#getting_credentials_for_server-centric_flow
.. _additional scopes: https://cloud.google.com/compute/docs/authentication#using
.. _Service Account key file: https://developers.google.com/identity/protocols/OAuth2ServiceAccount#creatinganaccount
