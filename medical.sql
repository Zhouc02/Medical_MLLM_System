-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: localhost    Database: medical
-- ------------------------------------------------------
-- Server version	8.0.37-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `doctor_help`
--

DROP TABLE IF EXISTS `doctor_help`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_help` (
  `from_id` int DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `add_time` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_help`
--

LOCK TABLES `doctor_help` WRITE;
/*!40000 ALTER TABLE `doctor_help` DISABLE KEYS */;
INSERT INTO `doctor_help` VALUES (10002,'请问主动脉突出还需要做什么检查？','2024年03月12日11:30'),(10003,'再看个CT吧','2024年03月12日11:35'),(10002,'肺结核需要看什么其它检查吗？','2024年05月24日16:15'),(10002,'好的，谢谢','2024年06月20日00:30'),(10002,'好的，谢谢','2024年06月20日00:34'),(10002,'已解决！','2024年06月20日00:57');
/*!40000 ALTER TABLE `doctor_help` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `from_id` int DEFAULT NULL,
  `to_id` int DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `add_time` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (10002,0,'请问为什么诊断速度有些变慢？','2024年05月04日22:25'),(10004,10002,'目前服务器负荷量较大，我们正在优化资源配置！','2024年05月04日22:34'),(10002,0,'好的，谢谢！','2024年06月20日00:03'),(10004,10002,'不客气','2024年06月20日00:11'),(10002,0,'嗯嗯','2024年06月20日00:15'),(10004,10002,'没事','2024年06月20日00:17'),(10004,10002,'嗯嗯','2024年06月20日00:21'),(10004,10002,'嗯嗯','2024年06月20日00:23'),(10002,0,'再见！','2024年06月20日00:57');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_analysis`
--

DROP TABLE IF EXISTS `log_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_analysis` (
  `job_id` varchar(255) NOT NULL,
  `add_time` varchar(255) DEFAULT NULL,
  `result` char(1) DEFAULT NULL,
  `content` text,
  `hive_sql` longtext,
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_analysis`
--

LOCK TABLES `log_analysis` WRITE;
/*!40000 ALTER TABLE `log_analysis` DISABLE KEYS */;
INSERT INTO `log_analysis` VALUES ('08e9c6a9-dc95-4d83-a','2023年12月20日12:10','Y','doctor	11\nsystem	77\n','import sys\nfor line in sys.stdin:\n    line = line.strip().split(\'|\')\n    print(\'{}\\t{}\'.format(line[0], 1)):::import sys\ntotal = 0\ntemp = \'\'\nfor line in sys.stdin:\n    word, count = line.strip().split(\'\\t\')\n    if word != temp and temp:\n        print(\'{}\\t{}\'.format(temp, total))\n        total = int(count)\n        temp = word\n    elif word == temp:\n        total += int(count)\n    else:\n        temp = word\n        total += int(count)\nprint(\'{}\\t{}\'.format(temp, total))','MapReduce'),('09a739c8-a9ea-486a-9','2024年05月24日16:17','Y','doctor	16\nsystem	27\n','import sys\nfor line in sys.stdin:\n    line = line.strip().split(\'|\')\n    print(\'{}\\t{}\'.format(line[0], 1)):::import sys\ntotal = 0\ntemp = \'\'\nfor line in sys.stdin:\n    word, count = line.strip().split(\'\\t\')\n    if word != temp and temp:\n        print(\'{}\\t{}\'.format(temp, total))\n        total = int(count)\n        temp = word\n    elif word == temp:\n        total += int(count)\n    else:\n        temp = word\n        total += int(count)\nprint(\'{}\\t{}\'.format(temp, total))','MapReduce'),('10615dc8-f8fa-46cf-a','2024年01月03日18:31','Y','doctor	3\nsystem	10\n','import sys\nfor line in sys.stdin:\n    line = line.strip().split(\'|\')\n    print(\'{}\\t{}\'.format(line[0], 1)):::import sys\ntotal = 0\ntemp = \'\'\nfor line in sys.stdin:\n    word, count = line.strip().split(\'\\t\')\n    if word != temp and temp:\n        print(\'{}\\t{}\'.format(temp, total))\n        total = int(count)\n        temp = word\n    elif word == temp:\n        total += int(count)\n    else:\n        temp = word\n        total += int(count)\nprint(\'{}\\t{}\'.format(temp, total))','MapReduce'),('13397161-c4c6-4fda-9','2024年01月03日18:28','Y','doctor	3\nsystem	9\n','select type,count(*) from logbaseMbUXnrXB group by type;','Hive'),('681c6d9a-4d1a-468e-9','2024年05月24日15:44','Y','doctor	10\nsystem	20\n','import sys\nfor line in sys.stdin:\n    line = line.strip().split(\'|\')\n    print(\'{}\\t{}\'.format(line[0], 1)):::import sys\ntotal = 0\ntemp = \'\'\nfor line in sys.stdin:\n    word, count = line.strip().split(\'\\t\')\n    if word != temp and temp:\n        print(\'{}\\t{}\'.format(temp, total))\n        total = int(count)\n        temp = word\n    elif word == temp:\n        total += int(count)\n    else:\n        temp = word\n        total += int(count)\nprint(\'{}\\t{}\'.format(temp, total))','MapReduce'),('a72e47a6-09b3-45d6-8','2023年12月29日19:49','Y','system	boot	/public/home/medical_2324/Medical_LLM/XrayGLM/checkpoints/xrayglm-3000	2023.12.29 19:47\nsystem	测试用户	Login	2023.12.29 19:47\n','select * from logbaseObPbSAXr','Hive');
/*!40000 ALTER TABLE `log_analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model`
--

DROP TABLE IF EXISTS `model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model` (
  `name` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `create_time` varchar(255) DEFAULT NULL,
  `create_manager` int DEFAULT NULL,
  `statu` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
INSERT INTO `model` VALUES ('medicalglm2','/root/Medical_LLM/VisualGLM/model/checkpoint/XrayGLM-3000','2023年12月23日00:01',10004,'Y');
/*!40000 ALTER TABLE `model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `token` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `self_id` varchar(255) DEFAULT NULL,
  `text_path` char(1) DEFAULT NULL,
  PRIMARY KEY (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES ('20240131143429186914_3y34Cu','张三','341225200000000000','Y'),('20240423205721290450_tkLPsQ','张三','341225200010100000','Y'),('20240504224010057361_McMVBA','张六','341225200205050011','Y'),('20240524161153847358_dth0qL','张三','341225200201010000','Y');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `auth` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10009 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (10002,'王五','e10adc3949ba59abbe56e057f20f883e','D'),(10003,'李四','e10adc3949ba59abbe56e057f20f883e','D'),(10004,'测试管理','e10adc3949ba59abbe56e057f20f883e','A'),(10005,'王小华','25d55ad283aa400af464c76d713c07ad','D');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-24 16:56:08
