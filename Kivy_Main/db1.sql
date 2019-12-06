-- MySQL dump 10.16  Distrib 10.1.37-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: db1
-- ------------------------------------------------------
-- Server version	10.1.37-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `jp_mst`
--

DROP TABLE IF EXISTS `jp_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jp_mst` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_fname` varchar(30) DEFAULT NULL,
  `p_mname` varchar(30) DEFAULT NULL,
  `p_lname` varchar(30) DEFAULT NULL,
  `p_height` int(3) DEFAULT NULL,
  `p_weight` int(3) DEFAULT NULL,
  `p_dob` varchar(11) DEFAULT NULL,
  `p_age` int(3) DEFAULT NULL,
  `p_gender` varchar(6) DEFAULT NULL,
  `p_smoke` varchar(3) DEFAULT NULL,
  `formatteddate` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jp_mst`
--

LOCK TABLES `jp_mst` WRITE;
/*!40000 ALTER TABLE `jp_mst` DISABLE KEYS */;
INSERT INTO `jp_mst` VALUES (1,'patient1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `jp_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jp_tx`
--

DROP TABLE IF EXISTS `jp_tx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jp_tx` (
  `sr_no` int(11) NOT NULL AUTO_INCREMENT,
  `p_id` int(30) DEFAULT NULL,
  `p_registration` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`sr_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jp_tx`
--

LOCK TABLES `jp_tx` WRITE;
/*!40000 ALTER TABLE `jp_tx` DISABLE KEYS */;
/*!40000 ALTER TABLE `jp_tx` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_info`
--

DROP TABLE IF EXISTS `patient_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `height` varchar(3) DEFAULT NULL,
  `weight` varchar(3) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` decimal(10,0) DEFAULT NULL,
  `smoker` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_info`
--

LOCK TABLES `patient_info` WRITE;
/*!40000 ALTER TABLE `patient_info` DISABLE KEYS */;
INSERT INTO `patient_info` VALUES (1,'Siddhi','155','48','female',22,'no'),(2,'charu','157','65','Female',54,'nnn'),(3,'Harshit	','160','67','Male',55,'no'),(4,'harshit','160','67','Male',56,'no'),(5,'patient1','162','55','Male',47,'yes'),(6,'patient2','155','78','Male',47,'no'),(7,'parth','165','56','Male',20,'no'),(8,'patoent1','34','34','Male',56,'no'),(9,'p2','156','67','Male',47,'no'),(10,'p3','150','56','Female',51,''),(11,'jahnvi','157','54','Female',27,'no'),(12,'riddhi','155','48','female',23,'no'),(13,'ronak','162','61','male',45,'yes'),(14,'siddhi','155','48','female',22,'no'),(15,'rani','160','78','female',63,'yes'),(16,'rani','160','78','female',63,'no'),(17,'raja','159','69','male',55,'no'),(18,'raja','159','69','male',55,'no'),(19,'mira','157','60','female',57,'no'),(20,'disha','156','56','female',28,'no'),(21,'rakesh','136','80','male',60,'no'),(22,'sirali','152','45','female',51,'no'),(23,'ronit','159','57','male',79,'no'),(24,'rakhi','159','58','female',38,'no'),(25,'shikha','158','54','female',23,'no'),(26,'rish','','','other',0,'rtu'),(27,'','','','',0,''),(28,'','','','',0,''),(29,'aa','22','22',NULL,NULL,NULL),(30,'aa','22','22',NULL,NULL,NULL),(31,'a','23','23',NULL,NULL,NULL),(32,'asv','24','34',NULL,NULL,NULL),(33,'','','','',0,'');
/*!40000 ALTER TABLE `patient_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-28 17:31:52
