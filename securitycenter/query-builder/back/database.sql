CREATE DATABASE IF NOT EXISTS query_builder;
CREATE USER IF NOT EXISTS 'proxyuser'@'localhost' IDENTIFIED BY 'kubernetes-test';
USE query_builder;
GRANT ALL ON query_builder.* TO "proxyuser"@"localhost";