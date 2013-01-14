# How to become a contributor and submit your own code

## Contributor License Agreements

We'd love to accept your sample apps and patches! However, before we can take them, we have to jump a couple of legal hurdles.

Please fill out either the individual or corporate Contributor License Agreement.

  * If you are an individual writing original source code and you're sure you own the intellectual property, then you'll need to sign an [individual CLA](http://code.google.com/legal/individual-cla-v1.0.html).
  * If you work for a company that wants to allow you to contribute your work the GoogleCloudPlatform organization, then you'll need to sign a [corporate CLA](http://code.google.com/legal/corporate-cla-v1.0.html).

Follow either of the two links above to access the appropriate CLA and instructions for how to sign and return it. Once we receive it, we'll add you to the official list of contributors and be able to accept your pull requests.

## Submitting Patches

1. Sign a Contributor License Agreement (see details above).
1. Coordinate your plans with team members that are listed on the repo in question. This ensures that work isn't being duplicated and communicating your plan early also generally leads to better patches.
1. Fork the desired repo, make and test your changes
1. Ensure that your code adheres to the existing style in the sample to which you are contributing. Refer to the [Google Cloud Platform Samples Style Guide](https://github.com/GoogleCloudPlatform/Home/wiki/STYLE.html) for the recommended coding standards for this organization. In the event the existing style conflicts with the recommended style, the former takes precedence over the latter.
1. Ensure that your code has an appropriate set of unit tests, which you have executed.
1. Submit a pull request. A pull request should address one issue in the repo. Please don't mix more than one logical change per pull request, because it makes the history hard to follow.

## Submitting a new sample app

Same procedure as for submitting patches, but with the additional provisions:

1. Send mail to one of the GoogleCloudPlatform owners with a short description of your proposed sample app.
1. If accepted, sign a Contributor License Agreement (see details above).
1. Clone the GoogleCloudPlatform/Home repo into a new repo. Follow this naming convention for your new repo:

{product}-{app-name}-{language}
products: appengine, compute, storage, bigquery, prediction, cloudsql
example:  appengine-guestbook-python
For multi-product apps, concatenate the primary products, like this: compute-appengine-demo-suite-python.
For multi-language apps, concatenate the primary languages like this: appengine-sockets-python-java-go.

1. Customize your README.md, LICENSE.md, CONTRIB.md, as needed.
1. Ensure that your code adheres to the recommended style guide for the language(s) you are using. Refer to the [Google Cloud Platform Samples Style Guide](https://github.com/GoogleCloudPlatform/Home/wiki/STYLE.html) for the recommended coding standards for this organization. In the event the existing style conflicts with the recommended style, the former takes precedence over the latter.
1. Ensure that your code has an appropriate set of unit tests, which you have executed.
1. Submit a pull request.
