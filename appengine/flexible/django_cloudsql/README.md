# Getting started with Django on Google Cloud Platform on App Engine Flexible

This repository is an example of how to run a [Django](https://www.djangoproject.com/) 
app on Google App Engine Flexible Environment. It uses the 
[Writing your first Django app](https://docs.djangoproject.com/en/1.9/intro/tutorial01/) as the 
example app to deploy.


## Setup the database

This tutorial assumes you are setting up Django using a SQL database, which is the easiest way to 
run Django.

* Create a [Second Generation CloudSQL instance](https://cloud.google.com/sql/docs/create-instance)

* Ensure the [Cloud SQL Administration API](https://console.cloud.google.com/flows/enableapi?apiid=sqladmin) is enabled.

* Install the [CloudSQL proxy](https://cloud.google.com/sql/docs/sql-proxy)

* Start the CloudSQL proxy using the connection string. The connection string can be obtained in the
instance details in the console. It's in the form of <project>:<region>:<instance-name>.
 
     ./cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306

* Create a root password

    `gcloud sql instances set-root-password [YOUR_INSTANCE_NAME] --password [YOUR_INSTANCE_ROOT_PASSWORD]`

* Use the root user and root password to create the `polls` database: 

    `mysql -h 127.0.0.1 -u root -p -e "CREATE DATABASE polls;"`

* Edit `app.yaml` to change the `cloud_sql_instances` to reflect the connection name of the 
instance. This is in the form project:zone:instance

* Optionally, use the root account to create a new MySQL user.

     `mysql -h 127.0.0.1 -u root -p -e "CREATE USER 'user'@'%' IDENTIFIED BY 'password';"  ``
     `mysql -h 127.0.0.1 -u root -p -e "GRANT ALL PRIVILEGES ON * . * TO 'user'@'%';" ``

Once you have a SQL host, configuring mysite/settings.py to point to your database. Change 
`your-cloudsql-connection-string` and `your-root-password`. If you created a new user and 
password, update those settings as well.

## Running locally

First make sure you have Django installed. It's recommended you do so in a 
[virtualenv](https://virtualenv.pypa.io/en/latest/). The requirements.txt
contains just the Django dependency.

    pip install -r requirements.txt

Once the database is setup, run the migrations.

    python manage.py makemigrations
    python manage.py makemigrations polls
    python manage.py migrate

If you'd like to use the admin console, create a superuser.

    python manage.py createsuperuser

The app can be run locally the same way as any other Django app. 

    python manage.py runserver

Now you can view the admin panel of your local site at http://localhost:8000/admin

## Deploying

The app can be deployed by running

    gcloud app deploy

You can view your site with:

    gcloud app browse

Now you can view the admin panel of your deployed site at https://<your-app-id>.appspot.com/admin


 ### Serving Static Files Using Cloud Storage

Since the Django development server is not built for production, our container uses the Gunicorn 
server. In `mysite/urls.py`, while in DEBUG mode, Django is configured to serve static files. 
 However, in production, it's recommended to use Google Cloud Storage or an alternative CDN for 
 serving static files. 

First, make a bucket and make it publically readable, replacing <your-gcs-bucket> with a bucket name
, such as your project id:

    gsutil mb gs://<your-gcs-bucket>
    gsutil defacl set public-read gs://<your-gcs-bucket>

Next, gather all the static content locally into one folder using the Django `collectstatic` command

    python manage.py collectstatic

Then upload it to CloudStorage using the `gsutil rsync` command

    gsutil rsync -R static/ gs://<your-gcs-bucket>/static

Now your static content can be served from the following URL:

    http://storage.googleapis.com/<your-gcs-bucket/static/

Make sure to replace <your-cloud-bucket> within `mysite/settings.py` to set STATIC_URL to the 
correct value to serve static content from, and uncomment the STATIC_URL to point to the new URL.

### Production

Once you are ready to serve your content in production, there are several
changes required for the configuration. Most notable changes are: 

* Use Google Cloud Storage or a CDN to serve static files
* Add ".appspot.com" to your `ALLOWED_HOSTS`
* Change the `DEBUG` variable to `False` in your settings.py file.

## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)


## Licensing

* See [LICENSE](LICENSE)
