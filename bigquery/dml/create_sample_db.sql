-- MySQL dump 10.13  Distrib 5.7.14, for osx10.11 (x86_64)
--
-- Host: 127.0.0.1    Database: sample_db
-- ------------------------------------------------------
-- Server version	5.7.14

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

--
-- Table structure for table `UserActions`
--

DROP TABLE IF EXISTS `UserActions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserActions` (
  `ActionID` int(11) NOT NULL AUTO_INCREMENT,
  `SessionID` varchar(36) DEFAULT NULL,
  `UserID` int(11) NOT NULL,
  `ActionType` varchar(64) NOT NULL DEFAULT '',
  `ActionTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Message` longtext,
  PRIMARY KEY (`ActionID`),
  KEY `SessionID` (`SessionID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `useractions_ibfk_2` FOREIGN KEY (`SessionID`) REFERENCES `UserSessions` (`SessionID`),
  CONSTRAINT `useractions_ibfk_3` FOREIGN KEY (`UserID`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=667621 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserActions`
--

LOCK TABLES `UserActions` WRITE;
/*!40000 ALTER TABLE `UserActions` DISABLE KEYS */;
/*!40000 ALTER TABLE `UserActions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserSessions`
--

DROP TABLE IF EXISTS `UserSessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserSessions` (
  `SessionID` varchar(36) NOT NULL DEFAULT '',
  `LoginTime` timestamp NULL DEFAULT NULL,
  `LogoutTime` timestamp NULL DEFAULT NULL,
  `IPAddress` varchar(40) DEFAULT '',
  `UserID` int(11) DEFAULT NULL,
  PRIMARY KEY (`SessionID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `usersessions_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserSessions`
--

LOCK TABLES `UserSessions` WRITE;
/*!40000 ALTER TABLE `UserSessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `UserSessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `UserID` int(11) NOT NULL,
  `DateJoined` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-02 12:39:19
