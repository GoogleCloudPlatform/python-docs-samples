## Google App Engine Managed VMs Python Hello World

This sample demonstrates using [Python on Google App Engine Managed VMs](https://cloud.google.com/appengine/docs/python/managed-vms/hello-world)

### Running & deploying the sample

1. `requirements.txt` is automatically installed by the runtime when deploying, however, to run the sample locally you will need to install dependencies:

        $ pip install -t lib -r requirements.txt

2. Run the sample on your development server:
        
        $ dev_appserver.py .

3. Deploy the sample:

        $ gcloud preview app deploy
