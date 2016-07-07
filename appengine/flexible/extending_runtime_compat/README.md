## Google App Engine Flexible Environment extending runtime python-compat

This sample demonstrates how to extend the [python-compat](https://cloud.google.com/appengine/docs/managed-vms/python/migrating-an-existing-app) runtime on [Google App Engine Flexible Environment](https://cloud.google.com/python/getting-started/hello-world)

### Running & deploying the sample

1. `requirements.txt` is automatically installed by the runtime when deploying, however, to run the sample locally you will need to install dependencies:

        $ pip install -r requirements.txt

2. Run the sample on your development server:
        
        $ dev_appserver.py --runtime python-compat .

3. Deploy the sample:

        $ gcloud app deploy
