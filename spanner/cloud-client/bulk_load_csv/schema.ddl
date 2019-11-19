/*
 Copyright 2019 Google Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 This application demonstrates how to do batch operations from a csv file
 using Cloud Spanner.
 For more information, see the README.rst.
*/
CREATE TABLE comments (
  id INT64,
  author STRING(MAX),
  `by` STRING(MAX),
  dead BOOL,
  deleted BOOL,
  parent INT64,
  ranking INT64,
  text STRING(MAX),
  time INT64,
  time_ts TIMESTAMP,
) PRIMARY KEY(parent, id);

CREATE INDEX CommentsByAuthor ON comments(author);

CREATE TABLE stories (
  id INT64,
  author STRING(MAX),
  `by` STRING(MAX),
  dead BOOL,
  deleted BOOL,
  descendants INT64,
  score INT64,
  text STRING(MAX),
  time INT64,
  time_ts TIMESTAMP,
  title STRING(MAX),
  url STRING(MAX),
) PRIMARY KEY(id);

CREATE INDEX StoriesByAuthor ON stories(author);

CREATE INDEX StoriesByScoreURL ON stories(score, url);

CREATE INDEX StoriesByTitleTimeScore ON stories(title) STORING (time_ts, score)
