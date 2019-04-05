-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: 172.17.0.2    Database: query_builder
-- ------------------------------------------------------
-- Server version	5.7.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Use database query_builder
CREATE DATABASE IF NOT EXISTS `query_builder` DEFAULT CHARACTER SET utf8;

USE `query_builder`;

--
-- Table structure for table `query`
--
DROP TABLE IF EXISTS `step`;

DROP TABLE IF EXISTS `query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `query` (
  `uuid` varchar(40) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  `topic` varchar(350) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `send_notification` tinyint(1) NOT NULL,
  `schedule` varchar(255) DEFAULT NULL,
  `next_run` datetime DEFAULT NULL,
  `last_execution_date` datetime DEFAULT NULL,
  `last_execution_result` int DEFAULT NULL,
  `last_execution_status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `query`
--

LOCK TABLES `query` WRITE;
/*!40000 ALTER TABLE `query` DISABLE KEYS */;
/*!40000 ALTER TABLE `query` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `step`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `step` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `order` int(11) NOT NULL,
  `scc_resource_type` varchar(255) NOT NULL,
  `filter` text DEFAULT NULL,
  `read_time_type` varchar(255) DEFAULT NULL,
  `read_time_value` varchar(255) DEFAULT NULL,
  `read_time_zone` varchar(255) DEFAULT NULL,
  `compare_duration` varchar(255) DEFAULT NULL,
  `in_value` text DEFAULT NULL,
  `out_value` text DEFAULT NULL,
  `threshold_operator` varchar(255) DEFAULT NULL,
  `threshold_value` varchar(255) DEFAULT NULL,
  `last_execution_result` int DEFAULT NULL,
  `last_execution_status` varchar(255) DEFAULT NULL,
  `query_id` varchar(40) NOT NULL,
  PRIMARY KEY (`_id`),
  KEY `step_query_id` (`query_id`),
  CONSTRAINT `step_ibfk_1` FOREIGN KEY (`query_id`) REFERENCES `query` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `step`
--

LOCK TABLES `step` WRITE;
/*!40000 ALTER TABLE `step` DISABLE KEYS */;
/*!40000 ALTER TABLE `step` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'query_builder'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-11 14:51:43
