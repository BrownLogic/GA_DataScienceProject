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
-- Table structure for table `bus_attributes`
--

DROP TABLE IF EXISTS `bus_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bus_attributes` (
  `business_id` varchar(250) NOT NULL,
  `attribute` varchar(250) NOT NULL,
  `attribute_value` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`business_id`,`attribute`),
  KEY `Bus_Attributes_attribute_index` (`attribute`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bus_categories`
--

DROP TABLE IF EXISTS `bus_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bus_categories` (
  `business_id` varchar(250) NOT NULL,
  `category` varchar(250) NOT NULL,
  PRIMARY KEY (`business_id`,`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bus_hours`
--

DROP TABLE IF EXISTS `bus_hours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bus_hours` (
  `business_id` varchar(250) NOT NULL,
  `day_of_week` varchar(250) NOT NULL,
  `open_time` varchar(250) DEFAULT NULL,
  `close_time` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`business_id`,`day_of_week`),
  KEY `Bus_hours_day_of_week_index` (`day_of_week`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bus_neighborhoods`
--

DROP TABLE IF EXISTS `bus_neighborhoods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bus_neighborhoods` (
  `business_id` varchar(250) NOT NULL,
  `neighborhood` varchar(250) NOT NULL,
  PRIMARY KEY (`business_id`,`neighborhood`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `business`
--

DROP TABLE IF EXISTS `business`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business` (
  `type` varchar(250) DEFAULT NULL,
  `business_id` varchar(250) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `city` varchar(250) DEFAULT NULL,
  `state` varchar(250) DEFAULT NULL,
  `latitude` decimal(20,16) DEFAULT NULL,
  `longitude` decimal(20,16) DEFAULT NULL,
  `stars` decimal(10,5) DEFAULT NULL,
  `review_count` int(11) DEFAULT NULL,
  `open` varchar(250) DEFAULT NULL,
  `full_address` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`business_id`),
  KEY `Business_city_index` (`city`),
  KEY `Business_stars_index` (`stars`),
  KEY `Business_state_index` (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cat_country_list`
--

DROP TABLE IF EXISTS `cat_country_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cat_country_list` (
  `alias` varchar(250) NOT NULL,
  `list_type` varchar(250) NOT NULL,
  `country` varchar(250) NOT NULL,
  PRIMARY KEY (`alias`,`list_type`,`country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cat_parents`
--

DROP TABLE IF EXISTS `cat_parents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cat_parents` (
  `alias` varchar(250) NOT NULL,
  `parent_alias` varchar(250) NOT NULL,
  PRIMARY KEY (`alias`,`parent_alias`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `alias` varchar(250) NOT NULL,
  `category` varchar(250) NOT NULL,
  PRIMARY KEY (`alias`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `checkins`
--

DROP TABLE IF EXISTS `checkins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `checkins` (
  `business_id` varchar(250) NOT NULL,
  `checkin_info` varchar(250) NOT NULL,
  `checkin_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`business_id`,`checkin_info`),
  KEY `Checkins_checkin_info_index` (`checkin_info`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `review` (
  `review_id` varchar(250) NOT NULL,
  `business_id` varchar(250) DEFAULT NULL,
  `user_id` varchar(250) DEFAULT NULL,
  `stars` decimal(10,5) DEFAULT NULL,
  `review_text` varchar(5000) DEFAULT NULL,
  `review_date` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `Review_Business_id_index` (`business_id`),
  KEY `Review_date_index` (`review_date`),
  KEY `Review_stars_index` (`stars`),
  KEY `Review_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `review_votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `review_votes` (
  `review_id` varchar(250) NOT NULL,
  `business_id` varchar(250) NOT NULL,
  `user_id` varchar(250) NOT NULL,
  `vote_type` varchar(250) NOT NULL,
  `vote_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`review_id`,`business_id`,`user_id`,`vote_type`),
  KEY `Review_Votes_Business_id_index` (`business_id`),
  KEY `Review_Votes_User_id_index` (`user_id`),
  KEY `Review_Votes_vote_type_index` (`vote_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `state_to_country`
--

DROP TABLE IF EXISTS `state_to_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `state_to_country` (
  `state` varchar(3) DEFAULT NULL,
  `country` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` varchar(250) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `review_count` int(11) DEFAULT NULL,
  `average_stars` decimal(10,5) DEFAULT NULL,
  `yelping_since` varchar(250) DEFAULT NULL,
  `fans` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_compliments`
--

DROP TABLE IF EXISTS `user_compliments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_compliments` (
  `user_id` varchar(250) NOT NULL,
  `compliment_type` varchar(250) NOT NULL,
  `compliment_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`compliment_type`),
  KEY `User_Compliments_compliment_type_index` (`compliment_type`),
  KEY `User_Compliments_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_elite`
--

DROP TABLE IF EXISTS `user_elite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_elite` (
  `user_id` varchar(250) NOT NULL,
  `years_elite` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`years_elite`),
  KEY `User_Elite_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_friends`
--

DROP TABLE IF EXISTS `user_friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_friends` (
  `user_id` varchar(250) NOT NULL,
  `friends` varchar(250) NOT NULL,
  PRIMARY KEY (`user_id`,`friends`),
  KEY `User_Friends_friends_index` (`friends`),
  KEY `User_Friends_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_tips`
--

DROP TABLE IF EXISTS `user_tips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tips` (
  `user_id` varchar(250) DEFAULT NULL,
  `business_id` varchar(250) DEFAULT NULL,
  `likes` int(11) DEFAULT NULL,
  `tip_date` varchar(250) DEFAULT NULL,
  `tip_text` varchar(5000) DEFAULT NULL,
  KEY `User_Tips_business_id_index` (`business_id`),
  KEY `User_Tips_tip_date_index` (`tip_date`),
  KEY `User_Tips_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_votes`
--

DROP TABLE IF EXISTS `user_votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_votes` (
  `user_id` varchar(250) NOT NULL,
  `vote_type` varchar(250) NOT NULL,
  `vote_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`vote_type`),
  KEY `User_Votes_user_id_index` (`user_id`),
  KEY `User_Votes_vote_type_index` (`vote_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `vw_business`
--

DROP TABLE IF EXISTS `vw_business`;
/*!50001 DROP VIEW IF EXISTS `vw_business`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_business` AS SELECT 
 1 AS `type`,
 1 AS `business_id`,
 1 AS `name`,
 1 AS `city`,
 1 AS `state`,
 1 AS `latitude`,
 1 AS `longitude`,
 1 AS `stars`,
 1 AS `review_count`,
 1 AS `open`,
 1 AS `full_address`,
 1 AS `country`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_confusion_matrix`
--

DROP TABLE IF EXISTS `vw_confusion_matrix`;
/*!50001 DROP VIEW IF EXISTS `vw_confusion_matrix`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_confusion_matrix` AS SELECT 
 1 AS `run_id`,
 1 AS `row_class`,
 1 AS `1_star`,
 1 AS `2_stars`,
 1 AS `3_stars`,
 1 AS `4_stars`,
 1 AS `5_stars`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_restaurant_categories`
--

DROP TABLE IF EXISTS `vw_restaurant_categories`;
/*!50001 DROP VIEW IF EXISTS `vw_restaurant_categories`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_restaurant_categories` AS SELECT 
 1 AS `category`,
 1 AS `alias`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_restaurants_in_usa`
--

DROP TABLE IF EXISTS `vw_restaurants_in_usa`;
/*!50001 DROP VIEW IF EXISTS `vw_restaurants_in_usa`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_restaurants_in_usa` AS SELECT 
 1 AS `review_id`,
 1 AS `business_id`,
 1 AS `user_id`,
 1 AS `stars`,
 1 AS `review_text`,
 1 AS `review_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_review_with_business_info`
--

DROP TABLE IF EXISTS `vw_review_with_business_info`;
/*!50001 DROP VIEW IF EXISTS `vw_review_with_business_info`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_review_with_business_info` AS SELECT 
 1 AS `review_id`,
 1 AS `user_id`,
 1 AS `stars`,
 1 AS `review_text`,
 1 AS `review_date`,
 1 AS `business_id`,
 1 AS `name`,
 1 AS `city`,
 1 AS `state`,
 1 AS `latitude`,
 1 AS `longitude`,
 1 AS `business_stars`,
 1 AS `review_count`,
 1 AS `open`,
 1 AS `full_address`,
 1 AS `country`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_runs_with_scores`
--

DROP TABLE IF EXISTS `vw_runs_with_scores`;
/*!50001 DROP VIEW IF EXISTS `vw_runs_with_scores`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_runs_with_scores` AS SELECT 
 1 AS `run_id`,
 1 AS `run_notes`,
 1 AS `classifier_info`,
 1 AS `avg_f1_score`,
 1 AS `avg_accuracy`,
 1 AS `test_time`,
 1 AS `train_time`,
 1 AS `class_label`,
 1 AS `f1_score`,
 1 AS `precision_score`,
 1 AS `recall_score`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vw_business`
--

/*!50001 DROP VIEW IF EXISTS `vw_business`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_business` AS select `business`.`type` AS `type`,`business`.`business_id` AS `business_id`,`business`.`name` AS `name`,`business`.`city` AS `city`,`business`.`state` AS `state`,`business`.`latitude` AS `latitude`,`business`.`longitude` AS `longitude`,`business`.`stars` AS `stars`,`business`.`review_count` AS `review_count`,`business`.`open` AS `open`,`business`.`full_address` AS `full_address`,`state_to_country`.`country` AS `country` from (`business` left join `state_to_country` on((`business`.`state` = `state_to_country`.`state`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_confusion_matrix`
--

/*!50001 DROP VIEW IF EXISTS `vw_confusion_matrix`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_confusion_matrix` AS select `t`.`run_id` AS `run_id`,`t`.`row_class` AS `row_class`,sum(`t`.`1_star`) AS `1_star`,sum(`t`.`2_stars`) AS `2_stars`,sum(`t`.`3_stars`) AS `3_stars`,sum(`t`.`4_stars`) AS `4_stars`,sum(`t`.`5_stars`) AS `5_stars` from (select `projectdb`.`model_confusion_matrix`.`run_id` AS `run_id`,`projectdb`.`model_confusion_matrix`.`row_class` AS `row_class`,(case when (`projectdb`.`model_confusion_matrix`.`col_class` = '1 star') then `projectdb`.`model_confusion_matrix`.`the_value` else 0 end) AS `1_star`,(case when (`projectdb`.`model_confusion_matrix`.`col_class` = '2 stars') then `projectdb`.`model_confusion_matrix`.`the_value` else 0 end) AS `2_stars`,(case when (`projectdb`.`model_confusion_matrix`.`col_class` = '3 stars') then `projectdb`.`model_confusion_matrix`.`the_value` else 0 end) AS `3_stars`,(case when (`projectdb`.`model_confusion_matrix`.`col_class` = '4 stars') then `projectdb`.`model_confusion_matrix`.`the_value` else 0 end) AS `4_stars`,(case when (`projectdb`.`model_confusion_matrix`.`col_class` = '5 stars') then `projectdb`.`model_confusion_matrix`.`the_value` else 0 end) AS `5_stars` from `projectdb`.`model_confusion_matrix`) `t` group by `t`.`run_id`,`t`.`row_class` order by `t`.`run_id`,`t`.`row_class` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_restaurant_categories`
--

/*!50001 DROP VIEW IF EXISTS `vw_restaurant_categories`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_restaurant_categories` AS select 'Restaurants' AS `category`,'restaurants' AS `alias` union select distinct `c`.`category` AS `category`,`t`.`category_alias` AS `alias` from (((select `p2`.`parent_alias` AS `parent2_alias`,`p1`.`parent_alias` AS `parent_alias`,`p1`.`alias` AS `category_alias` from ((`projectdb`.`cat_parents` `p1` left join `projectdb`.`cat_parents` `p2` on((`p2`.`alias` = `p1`.`parent_alias`))) left join `projectdb`.`cat_parents` `p3` on((`p3`.`alias` = `p2`.`parent_alias`))) where ('restaurants' in (`p1`.`parent_alias`,`p2`.`parent_alias`,`p3`.`parent_alias`)))) `t` join `projectdb`.`categories` `c` on((`t`.`category_alias` = `c`.`alias`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_restaurants_in_usa`
--

/*!50001 DROP VIEW IF EXISTS `vw_restaurants_in_usa`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_restaurants_in_usa` AS select `projectdb`.`review`.`review_id` AS `review_id`,`projectdb`.`review`.`business_id` AS `business_id`,`projectdb`.`review`.`user_id` AS `user_id`,`projectdb`.`review`.`stars` AS `stars`,`projectdb`.`review`.`review_text` AS `review_text`,`projectdb`.`review`.`review_date` AS `review_date` from `projectdb`.`review` where (`projectdb`.`review`.`business_id` in (select distinct `bc`.`business_id` from (`projectdb`.`bus_categories` `bc` join `projectdb`.`vw_restaurant_categories` `rc` on((`bc`.`category` = `rc`.`category`)))) and `projectdb`.`review`.`business_id` in (select `projectdb`.`business`.`business_id` from `projectdb`.`business` where (`projectdb`.`business`.`state` in ('AZ','CA','IL','MA','MN','NC','NV','OR','PA','SC','WA','WI')))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_review_with_business_info`
--

/*!50001 DROP VIEW IF EXISTS `vw_review_with_business_info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_review_with_business_info` AS select `r`.`review_id` AS `review_id`,`r`.`user_id` AS `user_id`,`r`.`stars` AS `stars`,`r`.`review_text` AS `review_text`,`r`.`review_date` AS `review_date`,`b`.`business_id` AS `business_id`,`b`.`name` AS `name`,`b`.`city` AS `city`,`b`.`state` AS `state`,`b`.`latitude` AS `latitude`,`b`.`longitude` AS `longitude`,`b`.`stars` AS `business_stars`,`b`.`review_count` AS `review_count`,`b`.`open` AS `open`,`b`.`full_address` AS `full_address`,`b`.`country` AS `country` from (`review` `r` join `vw_business` `b` on((`r`.`business_id` = `b`.`business_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_runs_with_scores`
--

/*!50001 DROP VIEW IF EXISTS `vw_runs_with_scores`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_runs_with_scores` AS select `runs`.`run_id` AS `run_id`,`runs`.`run_notes` AS `run_notes`,`runs`.`classifier_info` AS `classifier_info`,`runs`.`f1_score` AS `avg_f1_score`,`runs`.`accuracy` AS `avg_accuracy`,`runs`.`test_time` AS `test_time`,`runs`.`train_time` AS `train_time`,`scores`.`class_label` AS `class_label`,`scores`.`f1_score` AS `f1_score`,`scores`.`precision_score` AS `precision_score`,`scores`.`recall_score` AS `recall_score` from (`model_runs` `runs` join `model_scores` `scores` on((`runs`.`run_id` = `scores`.`run_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-02-15 14:00:53
