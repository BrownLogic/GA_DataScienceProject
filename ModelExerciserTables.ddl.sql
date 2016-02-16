-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: projectdb
-- ------------------------------------------------------
-- Server version	5.7.10-log

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
-- Table structure for table `model_confusion_matrix`
--

DROP TABLE IF EXISTS `model_confusion_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_confusion_matrix` (
  `run_id` int(11) NOT NULL,
  `row_class` varchar(500) NOT NULL,
  `col_class` varchar(500) NOT NULL,
  `the_value` int(11) DEFAULT NULL,
  PRIMARY KEY (`run_id`,`row_class`,`col_class`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `model_runs`
--

DROP TABLE IF EXISTS `model_runs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_runs` (
  `run_id` int(11) NOT NULL AUTO_INCREMENT,
  `run_time_stamp` datetime DEFAULT NULL,
  `train_time` decimal(13,3) DEFAULT NULL,
  `test_time` decimal(13,3) DEFAULT NULL,
  `accuracy` decimal(7,5) DEFAULT NULL,
  `f1_score` decimal(7,5) DEFAULT NULL,
  `classifier_info` varchar(5000) DEFAULT NULL,
  `run_notes` varchar(5000) DEFAULT NULL,
  `transform_info` varchar(5000) DEFAULT NULL,
  `data_info` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`run_id`),
  UNIQUE KEY `model_runs_run_id_uindex` (`run_id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `model_scores`
--

DROP TABLE IF EXISTS `model_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_scores` (
  `run_id` int(11) NOT NULL,
  `class_label` varchar(500) NOT NULL,
  `precision_score` decimal(4,3) DEFAULT NULL,
  `recall_score` decimal(4,3) DEFAULT NULL,
  `f1_score` decimal(4,3) DEFAULT NULL,
  PRIMARY KEY (`run_id`,`class_label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

