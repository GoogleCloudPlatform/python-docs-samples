## App Engine AngularJS "Hello World" Python

A simple [AngularJS](http://angularjs.org/) CRUD application
for [Google App Engine](https://appengine.google.com/).

Author: Fred Sauer <fredsa@google.com>


## Project setup

1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads)


## Testing the app locally

To run the app locally:

```
dev_appserver.py .
```


## Deploying

To deploy the application:

1. Use the [Google Cloud Console](https://cloud.google.com/console) to create a project
1. Replace `your-app-id` in `app.yaml` with the project id from the previous step
1. Deploy the application:

```
appcfg.py --oauth2 update .
```


## Contributing changes

See [CONTRIB.md](CONTRIB.md)


# Licensing

See [LICENSE](LICENSE)
