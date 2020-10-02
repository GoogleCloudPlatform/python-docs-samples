from django.db import migrations

import google.auth
from google.cloud import secretmanager_v1 as sm


def createsuperuser(apps, schema_editor):
    # Retrieve secret from Secret Manager 
    _, project = google.auth.default()
    client = sm.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/superuser_password/versions/latest"
    admin_password = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    # Create a new user using acquired password
    from django.contrib.auth.models import User
    User.objects.create_superuser("admin", password=admin_password)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunPython(createsuperuser)
    ]
