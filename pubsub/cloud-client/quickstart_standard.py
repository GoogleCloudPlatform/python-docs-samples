#!/usr/bin/env python

# Copyright 2018 Google LLC. All Rights Reserved.
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


import logging
import sys
import time
import multiprocessing as mp
import queue as Queue

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1 import types

mp.log_to_stderr()
logger = mp.get_logger()
logger.setLevel(logging.INFO)

NUM_MESSAGES = 2000
DATA = ('x' * 9500).encode('utf-8')

message_queue = mp.Queue()

subscribe_time = []

def publish(args):
    futures = []
    proj_id, topic_name = args

    publisher = pubsub_v1.PublisherClient(
        batch_settings=types.BatchSettings(max_messages=1000),)
    topic_path = publisher.topic_path(proj_id, topic_name)

    try:
        while True:
            message = message_queue.get(True, 1)
            start_time = time.time()
            future = publisher.publish(topic_path, str(message).encode('utf-8'))
            # Calculate publish time.
            dur = (time.time() - start_time)
            futures.append((future, [dur]))
    except Queue.Empty:
        pass

    results = []
    for f, dur in futures:
        start_time = time.time()
        f = f.result()
        # Calculate resolve time.
        dur.append(time.time() - start_time)
        results.append((f, dur))
    return results


def create_messages(args):
    """Populate the message queue"""
    for _ in range(NUM_MESSAGES):
        message_queue.put(DATA)


def subscribe(args):
    proj_id, sub_name = args

    def callback(message):
        temp = time.time()
        message.ack()
        # Calculate subscribe time.
        dur = time.time() - temp
        subscribe_time.append(dur)

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(proj_id, sub_name)
    subscriber.subscribe(subscription_path, callback=callback)

    while True:
        if len(subscribe_time) == NUM_MESSAGES:
            return sum(subscribe_time)
        else:
            time.sleep(5)

def main():
    pool = mp.Pool(8)

    # TODOs
    PROJECT_ID = 'tz-playground-bigdata'
    TOPIC_NAME = 'august'
    SUBSCRIPTION_NAME = 'one'

    # Create messages.
    pool.apply(create_messages, [()])

    # Publish messages.
    results = pool.apply(publish, [(PROJECT_ID, TOPIC_NAME)])

    # Subscribe to messages.
    sub_time = pool.apply(subscribe, [(PROJECT_ID, SUBSCRIPTION_NAME)])

    logger.info('Publish time for {} {:.0f}Kb messages: {:.6f}s'.format(
        len(results), sys.getsizeof(DATA)/1e3,
        sum([durs[0] for f,durs in results])))
    logger.info('Resolving tooking {:.6f}s'.format(
        sum([durs[1] for f,durs in results])))
    logger.info("Subscribing took {:.6f}s.".format(sub_time))


if __name__ == '__main__':
    main()
