#Retail Search Interactive Tutorials

##Run tutorials in Cloud Shell

To advance with the interactive tutorials, use Retail Search step-by-step manuals on the right side of the Cloud Shell IDE: 
![Interactive tutorials](images/tutorial1.png)

The interactive tutorial should open by default. If it didn’t, click on the Tutorial symbol in the menu bar to open the step-by-step manual:
![Toggle tutorial](images/tutorials2.png)

For more details about the Cloud Shell environment, refer to the [Cloud Shell documentation](https://cloud.google.com/shell/docs).

## Interactive tutorial flow

Interactive guides are intended to help you understand the features provided by Google Cloud Retail Search and test the Retail API in action.

To proceed with the tutorial, choose a language you’ll be deploying your project in:
![Select a programming language](images/tutorials3.png)


To begin with the tutorial workflow, click the Start button:
![Begin with the tutorial](images/tutorials4.png)

Then, you can use Next and Previous buttons to navigate the tutorial pages.

## Get started with the Google Cloud Retail API

The Retail API provides you with the following possibilities to: 
  - Create and maintaining the catalog data. 
  - Fine-tune the search configuration.
  - Import and maintain the user events data.

You can find the information about the Retail services in the [documentation](https://cloud.google.com/retail/docs)

<!--TODO(tkarasova) update the link to the tutorials when will be published-->
If you would like to have a closer look at the Retail API features and try them yourself,
the best option is to use the [Interactive Tutorials](https://cloud.google.com/retail/docs/overview). The tutorials will be launched in the CloudShell environment, and you will be able to request the Retail services and check the response with minimum time and effort.

The code samples in the directory **python-retail/samples/interactive-tutorials** are explicitly created for use with the Retail Interactive Tutorials.

If, for some reason, you have decided to proceed with these code samples without the tutorial, please go through the following steps and set up the required preconditions.

### Select your project and enable the Retail API

Google Cloud organizes resources into projects. This lets you
collect all related resources for a single application in one place.

If you don't have a Google Cloud project yet or you're not the owner of an existing one, you can
[create a new project](https://console.cloud.google.com/projectcreate).

After the project is created, set your PROJECT_ID to a ```project``` variable:

1. Run the following command in the Terminal:

    ```bash
    gcloud config set project <YOUR_PROJECT_ID>
    ```

1. Ensure that the Retail API is enabled for your project in the [API & Services page](https://console.cloud.google.com/apis/api/retail.googleapis.com/).

## Prepare your work environment

To prepare the work environment you should perform the following steps:
- Create a service account.
- Create service account key and set it to authorize your calls to the Retail API.
- Install Google Cloud Retail library.

### Create service account

To access the Retail API, you must create a service account. Check that you are an owner of your Google Cloud project on the [IAM page](https://console.cloud.google.com/iam-admin/iam).

1. To create a service account, perform the following command:

    ```bash
    gcloud iam service-accounts create <YOUR_SERVICE_ACCOUNT_ID>
    ```

1. Assign the needed roles to your service account:

    ```bash
    for role in {retail.admin,storage.admin}
    do gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> --member="serviceAccount:<YOUR_SERVICE_ACCOUNT_ID>@<YOUR_PROJECT_ID>.iam.gserviceaccount.com" --role="roles/${role}"
    done
    ```

1. Use the following command to print out the service account email:

    ```bash
    gcloud iam service-accounts list|grep <YOUR_SERVICE_ACCOUNT_ID>
    ```

    Copy the service account email.


1.  Upload your service account key JSON file and use it to activate the service
    account:

    ```bash
    gcloud iam service-accounts keys create ~/key.json --iam-account <YOUR_SERVICE_ACCOUNT_EMAIL>
    ```

    ```bash
    gcloud auth activate-service-account --key-file ~/key.json
    ```

1.  Set the key as the GOOGLE_APPLICATION_CREDENTIALS environment variable to
    use it for sending requests to the Retail API.

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS=~/key.json
    ```

### Install Google Cloud Retail libraries

To run Python code samples for the Retail API tutorial, you need to set up your virtual environment.

1. Run the following commands in a Terminal to create an isolated Python environment:

    ```bash
    virtualenv -p python3 myenv
    source myenv/bin/activate
    ```

1. Next, install Google packages:

    ```bash
    pip install google
    pip install google-cloud-retail
    pip install google-cloud-storage
    pip install google-cloud-bigquery

    ```

## Import catalog data

There is a python-retail/samples/interactive-tutorials/resources/products.json file with valid products prepared in the `resources` directory.

The other file, python-retail/samples/interactive-tutorials/resources/products_some_invalid.json, contains both valid and invalid products. You will use it to check the error handling.

### Upload catalog data to Cloud Storage

In your own project you need to create a Cloud Storage bucket and put the JSON file there.
The bucket name must be unique. For convenience, you can name it `<YOUR_PROJECT_ID>_<TIMESTAMP>`.

1. The code samples for each of the Retail services are stored in different directories.

    Go to the code samples directory, your starting point to run more commands.

    ```bash
    cd python-retail/samples/interactive-tutorials
    ```

1. To create the bucket and upload the JSON file, open python-retail/samples/interactive-tutorials/product/setup_product/products_create_gcs_bucket.py file

1. Go to the **product** directory and run the following command in the Terminal:

    ```bash
    python product/setup_product/products_create_gcs_bucket.py
    ```

    Now you can see the bucket is created in the [Cloud Storage](https://console.cloud.google.com/storage/browser), and the files are uploaded.

1. The name of the created Cloud Storage bucket is printed in the Terminal.

    ```
    The gcs bucket <YOUR_PROJECT_ID>_<TIMESTAMP> was created
    ```

    Copy the name and set it as the environment variable `BUCKET_NAME`:

    ```bash
    export BUCKET_NAME=<YOUR_BUCKET_NAME>
    ```

### Import products to the Retail Catalog

To import the prepared products to a catalog, open python-retail/samples/interactive-tutorials/product/import_products_gcs.py file and run the following command in the Terminal:

```bash
python product/import_products_gcs.py
```

## Run your code sample

Run the sample in a terminal with the following command:
```bash
python search/search_with_boost_spec.py
```