-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: escoot
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adminacc`
--

DROP TABLE IF EXISTS adminacc;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE adminacc (
  ID int NOT NULL,
  Username varchar(45) NOT NULL,
  `Password` varchar(45) NOT NULL,
  Picture_id int unsigned DEFAULT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminacc`
--

LOCK TABLES adminacc WRITE;
/*!40000 ALTER TABLE adminacc DISABLE KEYS */;
INSERT INTO adminacc VALUES (1,'Admin','Admin',1),(2,'Jerfel','Jef',2),(3,'Gil','Gil',3);
/*!40000 ALTER TABLE adminacc ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `balancecards`
--

DROP TABLE IF EXISTS balancecards;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE balancecards (
  Id int NOT NULL AUTO_INCREMENT,
  codes varchar(45) DEFAULT NULL,
  amount int DEFAULT NULL,
  PRIMARY KEY (Id),
  UNIQUE KEY codes_UNIQUE (codes)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `balancecards`
--

LOCK TABLES balancecards WRITE;
/*!40000 ALTER TABLE balancecards DISABLE KEYS */;
INSERT INTO balancecards VALUES (5,'a4kAPjU9RotV2cQP',60),(11,'ohKlBssXpqAC7cYx',20),(17,'CvHj34AvsfaOzvje',50),(21,'3mvYQ03RBshpGqlr',80),(22,'Q64ZKcIXWhRnYsLD',60),(24,NULL,NULL),(25,NULL,NULL),(26,NULL,NULL),(27,NULL,NULL),(28,NULL,NULL),(29,NULL,NULL),(30,NULL,NULL);
/*!40000 ALTER TABLE balancecards ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_history`
--

DROP TABLE IF EXISTS rental_history;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE rental_history (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  id_number varchar(255) NOT NULL,
  user_status varchar(10) DEFAULT 'Inactive',
  deducted_amount decimal(10,2) DEFAULT NULL,
  rental_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  user_time varchar(30) DEFAULT NULL,
  escoot_id varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_history`
--

LOCK TABLES rental_history WRITE;
/*!40000 ALTER TABLE rental_history DISABLE KEYS */;
INSERT INTO rental_history VALUES (24,'Jerfel','896754','Inactive',0.12,'2024-12-20 08:38:56','0 minutes 4 seconds','Scooter 1'),(25,'Jerfel','896754','Inactive',0.43,'2024-12-20 08:39:10','0 minutes 14 seconds','Scooter 13'),(26,'Jerfel','896754','Inactive',0.25,'2024-12-23 11:40:52','0 minutes 8 seconds','Scooter 13'),(27,'Jerfel','896754','Inactive',0.06,'2024-12-23 11:41:29','2.052264451980591','Scooter 13'),(28,'Jerfel','896754','Inactive',0.40,'2024-12-23 11:42:19','0 minutes 13 seconds','Scooter 14'),(29,'Jerfel','896754','Inactive',0.50,'2024-12-23 12:06:18','0 minutes 16 seconds','Scooter 1'),(30,'Jerfel','896754','Inactive',0.50,'2024-12-23 21:04:16','0 minutes 16 seconds','Scooter 1'),(31,'Jerfel','896754','Inactive',3.75,'2024-12-23 22:05:59','2 minutes 1 seconds','Scooter 1'),(32,'Jerfel','896754','Inactive',0.13,'2024-12-24 09:44:33','4.147580146789551','Scooter 1'),(33,'Jerfel','896754','Inactive',0.06,'2024-12-24 11:03:08','0 minutes 2 seconds','Scooter 2'),(34,'Jerfel','896754','Inactive',0.19,'2024-12-24 11:40:52','0 minutes 6 seconds','Scooter 2'),(35,'Kokomelon','051614','Inactive',0.25,'2024-12-24 22:17:13','0 minutes 8 seconds','Scooter 2'),(36,'KOKONUT','092312','Inactive',0.09,'2024-12-25 00:21:00','0 minutes 3 seconds','Scooter 2'),(37,'Jerfel','896754','Inactive',10000.00,'2024-12-25 00:24:19','0 minutes 25 seconds','Scooter 2'),(38,'Jerfel','896754','Inactive',0.09,'2024-12-25 03:05:53','0 minutes 3 seconds','Scooter 17'),(39,'KOKONUT','092312','Inactive',0.19,'2024-12-25 22:22:22','6.176677465438843','Scooter 2'),(40,'Kangaro','903212','Inactive',0.09,'2024-12-25 22:38:38','0 minutes 3 seconds','Scooter 3'),(41,'Jerfel','896754','Inactive',0.31,'2024-12-26 00:13:25','0 minutes 10 seconds','Scooter 3'),(42,'Jerfel','896754','Inactive',0.84,'2024-12-26 00:13:56','0 minutes 27 seconds','Scooter 3'),(43,'Jerfel','896754','Inactive',1.30,'2024-12-26 01:31:46','0 minutes 42 seconds','Scooter 14'),(44,'Jerfel','896754','Inactive',0.85,'2024-12-26 01:43:04','27.36547017097473','Scooter 3'),(45,'Jerfel','896754','Inactive',4.84,'2024-12-26 01:44:13','2 minutes 36 seconds','Scooter 4'),(46,'Jerfel','896754','Inactive',0.22,'2024-12-26 01:47:04','0 minutes 7 seconds','Scooter 4'),(47,'Jerfel','896754','Inactive',0.53,'2024-12-26 01:48:12','0 minutes 17 seconds','Scooter 4'),(48,'Jerfel','896754','Inactive',0.12,'2024-12-26 01:48:17','0 minutes 4 seconds','Scooter 4'),(49,'Jerfel','896754','Inactive',0.65,'2024-12-26 01:48:43','0 minutes 21 seconds','Scooter 4'),(50,'Jerfel','896754','Inactive',0.25,'2024-12-26 01:48:52','0 minutes 8 seconds','Scooter 4'),(51,'Jerfel','896754','Inactive',0.99,'2024-12-26 05:24:30','0 minutes 32 seconds','Scooter 1'),(52,'Jerfel','896754','Inactive',0.53,'2024-12-26 05:30:33','0 minutes 17 seconds','Scooter 2'),(53,'Jerfel','896754','Inactive',0.68,'2024-12-26 05:31:10','0 minutes 22 seconds','Scooter 2'),(54,'Jerfel','896754','Inactive',0.29,'2024-12-28 13:39:13','9.42544412612915','Scooter 1'),(55,'Jerfel','896754','Inactive',0.43,'2024-12-28 14:04:44','0 minutes 14 seconds','Scooter 1'),(56,'Jerfel','896754','Inactive',1.55,'2024-12-28 14:39:57','0 minutes 50 seconds','Scooter 1'),(57,'Jerfel','896754','Inactive',0.37,'2024-12-28 15:01:23','0 minutes 12 seconds','Scooter 1'),(58,'Jerfel','896754','Inactive',0.71,'2024-12-28 15:01:42','0 minutes 23 seconds','Scooter 1'),(59,'Jerfel','896754','Inactive',0.34,'2024-12-28 15:02:11','0 minutes 11 seconds','Scooter 1'),(60,'Jerfel','896754','Inactive',1.30,'2024-12-29 00:49:51','0 minutes 42 seconds','Scooter 1'),(61,'Jerfel','896754','Inactive',0.34,'2024-12-29 01:18:05','0 minutes 11 seconds','Scooter 1'),(62,'Jerfel','896754','Inactive',0.84,'2024-12-29 01:19:28','0 minutes 27 seconds','Scooter 1'),(63,'Jerfel','896754','Inactive',0.65,'2024-12-29 08:05:15','0 minutes 21 seconds','Scooter 1'),(64,'Jerfel','896754','Inactive',0.90,'2024-12-29 08:05:46','0 minutes 29 seconds','Scooter 1'),(65,'Jerfel','896754','Inactive',1.46,'2024-12-29 11:24:17','0 minutes 47 seconds','Scooter 1'),(66,'Jerfel','896754','Inactive',0.19,'2024-12-29 11:31:28','0 minutes 6 seconds','Scooter 1'),(67,'Jerfel','896754','Inactive',0.56,'2024-12-29 12:26:14','0 minutes 18 seconds','Scooter 1'),(68,'Jerfel','896754','Inactive',0.93,'2024-12-29 12:56:35','0 minutes 30 seconds','Scooter 2'),(69,'Jerfel','896754','Inactive',0.77,'2024-12-29 13:23:23','24.942258596420288','Scooter 1'),(70,'Jerfel','896754','Inactive',0.77,'2024-12-29 13:23:32','24.942258596420288','Scooter 1'),(71,'Jerfel','896754','Inactive',1.18,'2024-12-29 17:54:55','0 minutes 38 seconds','Scooter 1'),(72,'Jerfel','896754','Inactive',0.25,'2024-12-29 18:02:23','0 minutes 8 seconds','Scooter 1'),(73,'Jerfel','896754','Inactive',0.09,'2024-12-29 20:50:00','0 minutes 3 seconds','Scooter 1'),(74,'Jerfel','896754','Inactive',0.29,'2024-12-29 20:59:33','9.395519971847534','Scooter 1'),(75,'Jerfel','896754','Inactive',1.00,'2024-12-29 21:07:28','1','Scooter 2'),(76,'Jerfel','896754','Inactive',0.09,'2024-12-29 21:15:37','0 minutes 3 seconds','Scooter 3'),(77,'Jerfel','896754','Inactive',0.22,'2024-12-29 21:47:42','0 minutes 7 seconds','Scooter 1'),(78,'Jerfel','896754','Inactive',0.46,'2024-12-29 21:47:58','0 minutes 15 seconds','Scooter 1'),(79,'Jerfel','896754','Inactive',3.64,'2024-12-30 03:13:57','117.40371656417847','Scooter 1'),(80,'Kokomelon','051614','Inactive',2.39,'2024-12-30 03:15:16','1 minutes 17 seconds','Scooter 2'),(81,'Jerfel','896754','Inactive',0.55,'2024-12-30 03:27:57','17.690160751342773','Scooter 1'),(82,'Ooo','742464','Inactive',0.50,'2024-12-30 04:15:11','0 minutes 16 seconds','Scooter 1'),(83,'Jerfel','896754','Inactive',2.11,'2024-12-30 05:10:07','1 minutes 8 seconds','Scooter 1'),(84,'Kokomelon','051614','Inactive',0.37,'2024-12-30 05:10:48','0 minutes 12 seconds','Scooter 2'),(85,'Jerfel','896754','Inactive',8.09,'2024-12-30 05:59:34','4 minutes 21 seconds','Scooter 1'),(86,'Maamo','544207','Inactive',6.01,'2024-12-30 06:00:44','3 minutes 14 seconds','Scooter 2'),(87,'Jerfel','896754','Active',3.71,'2024-12-30 06:09:10','120.60966634750366','Scooter 1'),(88,'Kokomelon','051614','Inactive',1.18,'2024-12-31 14:04:28','0 minutes 38 seconds','Scooter 2'),(89,'Kokomelon','051614','Inactive',1.15,'2024-12-31 14:05:18','0 minutes 37 seconds','Scooter 2'),(90,'Kokomelon','051614','Inactive',0.12,'2024-12-31 14:14:10','0 minutes 4 seconds','Scooter 2'),(91,'Kokomelon','051614','Inactive',0.09,'2024-12-31 14:15:50','0 minutes 3 seconds','Scooter 2'),(92,'Kokomelon','051614','Inactive',2.23,'2024-12-31 14:17:40','1 minutes 12 seconds','Scooter 2');
/*!40000 ALTER TABLE rental_history ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `useracc`
--

DROP TABLE IF EXISTS useracc;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE useracc (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  phone varchar(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  id_number varchar(6) NOT NULL,
  Balance float DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id_number_UNIQUE (id_number)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `useracc`
--

LOCK TABLES useracc WRITE;
/*!40000 ALTER TABLE useracc DISABLE KEYS */;
INSERT INTO useracc VALUES (1,'Jerfel','09787865543','$2b$12$6A38baT2CReBEixUSpsqu.1cQwRUJ71y1wGXlGICrI6X7z2AGFGhe','896754',120),(3,'Kokomelon','09321287422','$2b$12$Ox1hR7eMm1xGMfScIzzRKuypbQIdWvumYoTKiBHS6fvHl3FbD5yCe','051614',-3.48895),(4,'Kangaro','90788932212','$2b$12$/rjBd6x03CJgavrJqsS0G.fFYb1uNJSsqvz1upzVO7e2llgdTxfwe','903212',29.5534),(5,'Jef','90321252321','$2b$12$FxOxVKdqEOMbeTpMjl.uVOxVrr1jseYNsrxO.SwupJ2DFBDwbND8S','213242',80.661),(6,'KOKONUT','90322124893','$2b$12$xk5X25.0Qh.Ob3zIN0IVveXvb45IKYXkJy0tALFarvetUXBId5OA6','092312',99.6208),(9,'Robert','90322132241','$2b$12$6Xg28wyiQK6IAkd1a8C3UOy8W8h/UxYR.wBMfy.YDEESq2jEo6.Tu','392142',100),(10,'Ooo','09234212521','$2b$12$8rb3O5yHdEFuuFaUzVRHs.6xsPrxR5FoUvCbvlnjYe1EO9mvJueUC','742464',19.0191);
/*!40000 ALTER TABLE useracc ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-31 22:31:37
