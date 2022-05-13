# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.conf.urls import url
from django.conf import settings
from google.appengine.api import wrap_wsgi_app
from google.appengine.api import mail
from google.cloud import logging

# Logging client in Python 3
logging_client = logging.Client()

# This log can be found in the Cloud Logging console under 'Custom Logs'.
logger = logging_client.logger("django-app-logs")

def receive_mail(request):
    mail_message = mail.InboundEmailMessage(request.body)
    # Make a simple text log
    logger.log_text('Received greeting at %s from %s: %s' % (
        mail_message.to,
        mail_message.sender,
        mail_message.bodies('text/plain')))
    return HttpResponse('Success')

def receive_bounce(request):
    bounce_message = mail.BounceNotification(dict(request.POST.lists()))

    # Make a simple text log
    logger.log_text('Bounce original: %s' % (bounce_message.__original))
    logger.log_text('Bounce notification: %s' % (bounce_message.__notification))

    return HttpResponse('Success')

urlpatterns = (
    url(r'_ah/mail/.*$', receive_mail),
    url(r'_ah/bounce', receive_bounce),
)

settings.configure(
    DEBUG=True,
    SECRET_KEY='thisisthesecretkey',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

app = wrap_wsgi_app(get_wsgi_application())
