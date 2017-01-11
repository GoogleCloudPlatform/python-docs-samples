## Note

This sample demonstrates connecting to existing Memcache servers, or the
built-in Memcache server.

A managed option for Memcache is RedisLabs:

https://cloud.google.com/appengine/docs/flexible/python/using-redislabs-memcache

You can install and manage a Memcache server on Google Compute Engine. One way
to do so is to use a Bitnami click-to-deploy:

https://bitnami.com/stack/memcached/cloud/google

Built-in Memcache for Flexible environments is currently in a whitelist-only alpha. To have your project whitelisted,
see the signup form here:

https://cloud.google.com/appengine/docs/flexible/python/upgrading#memcache_service

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

When running locally, you can use the [Google Cloud SDK](https://cloud.google.com/sdk) to provide authentication to use Google Cloud APIs:

    $ gcloud init

Install dependencies, preferably with a virtualenv:

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Start your application:

    $ python main.py

## Deploying on App Engine

Deploy using `gcloud`:

    gcloud app deploy

You can now access the application at `https://your-app-id.appspot.com`.
