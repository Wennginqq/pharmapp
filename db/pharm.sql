CREATE DATABASE  IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `mydb`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.2.0

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
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `age` varchar(45) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `email` varchar(45) NOT NULL,
  `speciality` varchar(45) NOT NULL,
  `user_type_id_user_type` int NOT NULL,
  `hours_worked` int DEFAULT '0',
  PRIMARY KEY (`doctor_id`),
  KEY `fk_doctor_user_type1_idx` (`user_type_id_user_type`),
  CONSTRAINT `fk_doctor_user_type1` FOREIGN KEY (`user_type_id_user_type`) REFERENCES `user_type` (`id_user_type`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (1,'avin1','avin1','Семен','Иванов','45','89212495245','avin@hosp.com','Заведующий терапевтическим отделением',1,36),(2,'kokina','kokina','Наталья','Кокошко','52','89133294123','kokina@hosp.com','Заведующая хирургическим отделением',1,123),(3,'anisimov','anisimov','Николай','Анисимов','32','89211923456','nikoani@hosp.com','Терапевт',3,41),(4,'arimova','arimova','Наталья','Аримова','23','89122393423','arimova@hosp.com','Медсестра',2,52),(5,'aben','aben','Андрей','Абин','35','89123453245','aben@doct.com','медбрат',2,55);
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `age` int DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `passport` varchar(10) NOT NULL,
  `user_type_id_user_type` int NOT NULL,
  PRIMARY KEY (`patient_id`),
  KEY `fk_patient_user_type_idx` (`user_type_id_user_type`),
  CONSTRAINT `fk_patient_user_type` FOREIGN KEY (`user_type_id_user_type`) REFERENCES `user_type` (`id_user_type`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'karton','karton','Семен','Картонов',21,'89142452345','1029348271',4),(2,'makoro','makoro','Екатерина','Королева',32,'8912345265','2837458273',4),(3,'alex1','alex1','Антон','Алексеевич',32,'89141923456','1234567890',4);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `date_of_creation` datetime DEFAULT NULL,
  `caption` varchar(255) DEFAULT 'не заполнено',
  `patient_patient_id` int DEFAULT NULL,
  `doctor_doctor_id` int DEFAULT NULL,
  `service_service_id` int DEFAULT NULL,
  `service_status_id_service_status` int DEFAULT NULL,
  PRIMARY KEY (`record_id`),
  KEY `fk_records_patient1_idx` (`patient_patient_id`),
  KEY `fk_records_doctor1_idx` (`doctor_doctor_id`),
  KEY `fk_records_service1_idx` (`service_service_id`),
  KEY `fk_records_service_status1_idx` (`service_status_id_service_status`),
  CONSTRAINT `fk_records_doctor1` FOREIGN KEY (`doctor_doctor_id`) REFERENCES `doctor` (`doctor_id`),
  CONSTRAINT `fk_records_patient1` FOREIGN KEY (`patient_patient_id`) REFERENCES `patient` (`patient_id`),
  CONSTRAINT `fk_records_service1` FOREIGN KEY (`service_service_id`) REFERENCES `service` (`service_id`),
  CONSTRAINT `fk_records_service_status1` FOREIGN KEY (`service_status_id_service_status`) REFERENCES `service_status` (`id_service_status`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` VALUES (1,'2023-01-19 03:14:07','не заполнено',1,1,1,1),(2,'2023-01-19 03:14:07','Пациент не пришел',2,2,2,3),(3,'2023-11-14 07:04:00','не заполнено',1,2,2,1);
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_name` varchar(45) NOT NULL,
  `price` double NOT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (1,'консультация у терапевта',3000),(2,'консультация у хирурга',3000),(3,'консультация у невролога',3000),(4,'УЗИ',6000),(5,'МРТ',3000);
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_status`
--

DROP TABLE IF EXISTS `service_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_status` (
  `id_service_status` int NOT NULL AUTO_INCREMENT,
  `service_status` varchar(45) NOT NULL,
  PRIMARY KEY (`id_service_status`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_status`
--

LOCK TABLES `service_status` WRITE;
/*!40000 ALTER TABLE `service_status` DISABLE KEYS */;
INSERT INTO `service_status` VALUES (1,'Выполнено'),(2,'Создано'),(3,'Отменено');
/*!40000 ALTER TABLE `service_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_type`
--

DROP TABLE IF EXISTS `user_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_type` (
  `id_user_type` int NOT NULL AUTO_INCREMENT,
  `user_type` varchar(45) NOT NULL,
  PRIMARY KEY (`id_user_type`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_type`
--

LOCK TABLES `user_type` WRITE;
/*!40000 ALTER TABLE `user_type` DISABLE KEYS */;
INSERT INTO `user_type` VALUES (1,'Главный администратор'),(2,'Младший администратор'),(3,'Врач'),(4,'Пациент');
/*!40000 ALTER TABLE `user_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-12 14:28:54
