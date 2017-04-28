# Copyright 2015 Google Inc.
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

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .models import Message

from django.core.cache import cache

import math
import logging

def __update_visited():
    """ Updates the visited count by one in the cache
    :return: The visited count in string form.
    """
    visited = cache.get('visited')
    if not visited:
        visited = 0
    else:
        visited = int(visited)
    visited += 1
    cache.set('visited', str(visited))
    return str(visited)


def index(request):
    """ Updates the visited count and provides the static URL to build the main
     landing page.
    """
    logging.info("in the index view")
    visited = __update_visited()
    context = {
                 "STATIC_URL": settings.STATIC_URL,
                 "visited": visited
               }
    return render(request, 'index.html', context)


def messages(request):
    """ REST endpoint providing basic operations. GET will return the list of
    all messages created so far in JSON form, POST will add a new message to
    the list of messages (guestbook).
    """
    if request.method == 'GET':
        data = serializers.serialize("json", Message.objects.all())
        return HttpResponse(data)
    elif request.method == 'POST':
        Message.objects.create(text=request.body)
        return HttpResponse(request.body)
    else:
        return HttpResponse("Unsupported HTTP Verb.")


def compute(request):
    """ Endpoint that does some CPU intensive work to help demonstrate
     autoscaling.
    """
    logging.info("doing some long calculations")
    x = 0.0001
    for i in range(0, 1000000):
        x += math.sqrt(x)
    return HttpResponse("Performed a lot of work")
