# Getting started with Django on Google Cloud Platform

This repository is an example of how to run a [Django](https://www.djangoproject.com/) 
app on Google App Engine Flexible Environment. It uses the [Writing your first Django app](https://docs.djangoproject.com/en/1.9/intro/tutorial01/) as the example app to deploy.


## Setup the database

This tutorial assumes you are setting up Django using a SQL database, which is the easiest way to run Django. If you have an existing SQL database running, you can use that, but if not, these are the instructions for creating a managed MySQL instance using CloudSQL.


* Create a [CloudSQL instance](https://console.cloud.google.com/project/_/sql/create)

    * In the instances list, click your Cloud SQL instance.

    * Click Access Control.

    * In the IP address subsection, click Request an IPv4 address to enable access to the Cloud SQL instance through an 
    IPv4 address. It will take a moment to initialize the new IP address.

    * Also under Access Control, in the Authorization subsection, under Allowed Networks, click the add (+) button .

    * In the Networks field, enter 0.0.0.0/0. This value allows access by all IP addresses.

    * Click Save.

Note: setting allowed networks to 0.0.0.0/0 opens your SQL instance to traffic from any computer. For production databases, it's highly recommended to limit the authorized networks to only IP ranges that need  access.

* Alternatively, the instance can be created with the gcloud command line tool as follows, substituting `your-root-pw
 with a strong, unique password.

        gcloud sql instances create <instance_name> --assign-ip --authorized-networks=0.0.0.0/0  set-root-password=your-root-pw

* Create a Database And User

    * Using the root password created in the last step to create a new database, user, and password using your preferred MySQL client. Alternatively, follow these instructions to create the database and user from the console.
        * From the CloudSQL instance in the console,  click New user.
        * Enter a username and password for the application. For example, name the user "pythonapp" and give it a randomly 
       generated password.
        * Click Add.
        * Click Databases and then click New database.
        * For Name, enter the name of your database (for example, "polls"), and click Add.

Once you have a SQL host, configuring mysite/settings.py to point to your database. Change `your-database-name`, 
`your-database-user`, `your-database-host` , and `your-database-password` to match the settings created above. Note the 
instance name is not used in this configuration, and the host name is the IP address you created.

## Running locally

First make sure you have Django installed. It's recommended you do so in a 
[virtualenv](https://virtualenv.pypa.io/en/latest/). The requirements.txt
contains just the Django dependency.

    pip install -r requirements.txt

Once the database is setup, run the migrations.

    python manage.py migrate

If you'd like to use the admin console, create a superuser.

    python manage.py createsuperuser

The app can be run locally the same way as any other Django app. 

    python manage.py runserver

Now you can view the admin panel of your local site at http://localhost:8080/admin

## Deploying

Since the Django development server is not built for production, our container uses the Gunicorn server. Since Gunicorn doesn't serve static content,
the static content is instead served from Google Cloud Storage.

First, make a bucket and make it publically readable, replacing <your-gcs-bucket> with a bucket name, such as your project id:

    gsutil mb gs://<your-gcs-bucket>
    gsutil defacl set public-read gs://<your-gcs-bucket>

Next, gather all the static content locally into one folder using the Django `collectstatic` command

    python manage.py collectstatic

Then upload it to CloudStorage using the `gsutil rsync` command

    gsutil rsync -R static/ gs://<your-gcs-bucket>/static

Now your static content can be served from the following URL:

    http://storage.googleapis.com/<your-gcs-bucket/static/

Make sure to replace <your-cloud-bucket> within `mysite/settings.py` to set STATIC_URL to the correct value to serve static content from, and
uncomment the STATIC_URL to point to the new URL.

The app can be deployed by running

    gcloud app deploy
    
which deploys to version 1, and `promote` makes version 1 the default version.

Now you can view the admin panel of your deployed site at https://<your-app-id>.appspot.com/admin.

### Production

Once you are ready to serve your content in production, there are several
changes required for the configuration. Most notable changes are: 
* Add ".appspot.com" to your `ALLOWED_HOSTS`
* Change the `DEBUG` variable to `False` in your settings.py file.
* If you are using a Cloud SQL database
instance, in order to change from `DEBUG = True`
to `DEBUG = False` you will need to properly configure the database. See
instructions
[here](https://cloud.google.com/sql/docs/app-engine-connect#gaev2-csqlv2) and be
sure to change your `app.yaml` file as well as the `HOST` key in your
`DATABASES` object.
 

## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)


## Licensing

* See [LICENSE](LICENSE)
