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
