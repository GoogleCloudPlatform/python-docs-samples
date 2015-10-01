## Google App Engine Managed VMs Python Hello World

This sample demonstrates using [Python on Google App Engine Managed VMs](https://cloud.google.com/appengine/docs/python/managed-vms/hello-world)

### Running & deploying the sample

1. Requirements.txt is not automatically processed by Google App Engine Managed VMs. To install dependencies for this sample, run:

        $ pip install -t lib -r requirements.txt

2. Run the sample on your development server:
        
        $ dev_appserver.py .

3. Deploy the sample:

        $ appcfg.py update -A your-app-id .
