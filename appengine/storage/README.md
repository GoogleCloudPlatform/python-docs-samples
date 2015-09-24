## Google App Engine using Cloud Storage

This sample demonstrates how to use Google Cloud Storage from Google App Engine

### Running the sample

1. To install dependencies for this sample, run:

        $ pip install -t lib -r requirements.txt

2. You must then update `main.py` and replace `<your-bucket-name>` with your Cloud Storage bucket.

3. You can then run the sample on your development server:
        
        $ dev_appserver.py .

   Or deploy the application:

        $ appcfg.py update .
