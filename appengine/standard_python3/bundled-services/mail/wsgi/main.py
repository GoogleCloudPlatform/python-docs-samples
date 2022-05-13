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

from google.appengine.api import wrap_wsgi_app
from google.appengine.api import mail
import re, http


def HelloReceiver(environ, start_response):
  if environ['REQUEST_METHOD'] != 'POST':
    return ('', http.HTTPStatus.METHOD_NOT_ALLOWED, [('Allow', 'POST')])

  mail_message = mail.InboundEmailMessage.from_environ(environ)
  
  # Do something with the message
  print('Received greeting from %s: %s' % (mail_message.sender, mail_message.body))

  # Return suitable response
  response = http.HTTPStatus.OK
  start_response(f'{response.value} {response.phrase}', [])
  return ['success'.encode('utf-8')]

def BounceReceiver(environ, start_response):
  if environ['REQUEST_METHOD'] != 'POST':
    return ('', http.HTTPStatus.METHOD_NOT_ALLOWED, [('Allow', 'POST')])

  bounce_message = mail.BounceNotification.from_environ(environ)
  
  # Do something with the message
  print('Received bounce post.')
  print('Bounce original: %s', bounce_message.original)
  print('Bounce notification: %s', bounce_message.notification)

  # Return suitable response
  response = http.HTTPStatus.OK
  start_response(f'{response.value} {response.phrase}', [])
  return ['success'.encode('utf-8')]

def InvalidMailSender(environ, start_response):
  # Send invalid mail to trigger a bounce notification.
  mail.send_mail(sender="test-python-user@shreejad-knative-dev.appspotmail.com",
                   to="Invalid Address <random-bounce@gmail.com>",
                   subject="Test Email Subject sd",
                   body="Test Email Body sd")
    
  print('Successfully sent a mail to random-bounce@gmail.com.')
  print('This should trigger a bounce notification.')

  # Return suitable response
  response = http.HTTPStatus.OK
  start_response(f'{response.value} {response.phrase}', [])
  return ['success'.encode('utf-8')]

routes = {
            mail.INCOMING_MAIL_URL_PATTERN: HelloReceiver,
            mail.BOUNCE_NOTIFICATION_URL_PATH: BounceReceiver,
            'send_invalid_mail': InvalidMailSender
         }

class WSGIApplication():
  def __call__(self, environ, start_response):
    path = environ.get('PATH_INFO', '')
    for regex, callable in routes.items():
      match = re.search(regex, path)
      if match is not None:
        return callable(environ, start_response)

app = wrap_wsgi_app(WSGIApplication())
