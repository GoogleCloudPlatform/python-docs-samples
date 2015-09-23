#!/usr/bin/env python
#
# Copyright 2012 Google Inc.
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
#
"""Sample app demonstrates extraction of GAE Datastore data to Google BigQuery

Uses the App Engine MapReduce mapper pipeline to read entities
out of the App Engine Datastore, write processed entities into
Cloud Storage in CSV format, then starts another pipeline that
creates a BigQuery ingestion job. Uses code from the log2bq
project: http://code.google.com/p/log2bq/
"""


__author__ = 'manoochehri@google.com (Michael Manoochehri)'


import time
import calendar
import datetime
import httplib2

from google.appengine.api import taskqueue
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from mapreduce.lib import files
from mapreduce import base_handler
from mapreduce import mapreduce_pipeline

from apiclient.discovery import build
from oauth2client.appengine import AppAssertionCredentials


SCOPE = 'https://www.googleapis.com/auth/bigquery'
PROJECT_ID = 'XXXXXXXXXXXX' # Your Project ID here
BQ_DATASET_ID = 'datastore_data'
GS_BUCKET = 'datastore_csvoutput'
ENTITY_KIND = 'main.ProductSalesData'


class ProductSalesData(db.Model):
  product_id = db.IntegerProperty(required=True)
  date = db.DateTimeProperty(verbose_name=None,
                             auto_now=True,
                             auto_now_add=True)
  store = db.StringProperty(required=True)


class DatastoreMapperPipeline(base_handler.PipelineBase):
  def run(self, entity_type):
    output = yield mapreduce_pipeline.MapperPipeline(
      "Datastore Mapper %s" % entity_type,
      "main.datastore_map",
      "mapreduce.input_readers.DatastoreInputReader",
      output_writer_spec="mapreduce.output_writers.FileOutputWriter",
      params={
          "input_reader":{
              "entity_kind": entity_type,
              },
          "output_writer":{
              "filesystem": "gs",
              "gs_bucket_name": GS_BUCKET,
              "output_sharding":"none",
              }
          },
          shards=12)
    yield CloudStorageToBigQuery(output)


class CloudStorageToBigQuery(base_handler.PipelineBase):
  def run(self, csv_output):

    credentials = AppAssertionCredentials(scope=SCOPE)
    http = credentials.authorize(httplib2.Http())
    bigquery_service = build("bigquery", "v2", http=http)

    jobs = bigquery_service.jobs()
    table_name = 'datastore_data_%s' % datetime.datetime.utcnow().strftime(
        '%m%d%Y_%H%M%S')
    files = [str(f.replace('/gs/', 'gs://')) for f in csv_output]
    result = jobs.insert(projectId=PROJECT_ID,
                        body=build_job_data(table_name,files))
    result.execute()


def build_job_data(table_name, files):
  return {"projectId": PROJECT_ID,
          "configuration":{
              "load": {
                  "sourceUris": files,
                  "schema":{
                      "fields":[
                          {
                              "name":"product_id",
                              "type":"INTEGER",
                          },
                          {
                              "name":"date",
                              "type":"INTEGER",
                          },
                          {
                              "name":"store",
                              "type":"STRING",
                          }
                          ]
                      },
                  "destinationTable":{
                      "projectId": PROJECT_ID,
                      "datasetId": BQ_DATASET_ID,
                      "tableId": table_name,
                      },
                  "maxBadRecords": 0,
                  }
              }
          }


def datastore_map(entity_type):
  data = db.to_dict(entity_type)
  resultlist = [data.get('product_id'),
                timestamp_to_posix(data.get('date')),
                data.get('store')]
  result = ','.join(['"%s"' % field for field in resultlist])
  yield("%s\n" % result)


def timestamp_to_posix(timestamp):
  return int(time.mktime(timestamp.timetuple()))


class DatastoretoBigQueryStart(webapp.RequestHandler):
  def get(self):
    pipeline = DatastoreMapperPipeline(ENTITY_KIND)
    pipeline.start()
    path = pipeline.base_path + "/status?root=" + pipeline.pipeline_id
    self.redirect(path)

  
class AddDataHandler(webapp.RequestHandler):
  def get(self):
    for i in range(0,9):
      data = ProductSalesData(product_id=i,
                              store='Store %s' % str(i))
      self.response.out.write('Added sample Datastore entity #%s<br />' % str(i))
      data.put()
    self.response.out.write('<a href="/start">Click here</a> to start the Datastore to BigQuery pipeline.')


application = webapp.WSGIApplication(
                                     [('/start', DatastoretoBigQueryStart),
                                      ('/add_data', AddDataHandler)],
                                      debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
