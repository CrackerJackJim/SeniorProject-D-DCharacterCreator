CREATE DATABASE  IF NOT EXISTS `dnd` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dnd`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: dnd
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `ability_scores`
--

DROP TABLE IF EXISTS `ability_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ability_scores` (
  `CharacterID` int NOT NULL,
  `Strength` int NOT NULL DEFAULT '10',
  `Dexterity` int NOT NULL DEFAULT '10',
  `Constitution` int NOT NULL DEFAULT '10',
  `Intelligence` int NOT NULL DEFAULT '10',
  `Wisdom` int NOT NULL DEFAULT '10',
  `Charisma` int NOT NULL DEFAULT '10',
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `ability_scores_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ability_scores`
--

LOCK TABLES `ability_scores` WRITE;
/*!40000 ALTER TABLE `ability_scores` DISABLE KEYS */;
/*!40000 ALTER TABLE `ability_scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `abilityscores`
--

DROP TABLE IF EXISTS `abilityscores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `abilityscores` (
  `AbilityScoreID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `StrScore` int NOT NULL,
  `StrMod` int NOT NULL,
  `DexScore` int NOT NULL,
  `DexMod` int NOT NULL,
  `ConScore` int NOT NULL,
  `ConMod` int NOT NULL,
  `IntScore` int NOT NULL,
  `IntMod` int NOT NULL,
  `WisScore` int NOT NULL,
  `WisMod` int NOT NULL,
  `ChaScore` int NOT NULL,
  `ChaMod` int NOT NULL,
  PRIMARY KEY (`AbilityScoreID`),
  KEY `CharacterID` (`CharacterID`),
  CONSTRAINT `abilityscores_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abilityscores`
--

LOCK TABLES `abilityscores` WRITE;
/*!40000 ALTER TABLE `abilityscores` DISABLE KEYS */;
/*!40000 ALTER TABLE `abilityscores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `AccountID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `PasswordHash` varchar(255) NOT NULL,
  `AccountType` enum('Guest','Registered') NOT NULL DEFAULT 'Registered',
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`AccountID`),
  UNIQUE KEY `ux_account_username` (`Username`),
  UNIQUE KEY `ux_account_email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (3,'Test','dtate9@atu.edu','$argon2id$v=19$m=65536,t=3,p=4$x5iTco7x3tt7T2ntfY+Rsg$OJGO6BWuYSja76LGCHb/hGvxRfC6ILH+uQUW8yWe62w','Registered','2026-02-03 20:38:10','2026-03-08 20:21:21'),(4,'Test1','daltontate11@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$fO+d896bc6517h3DGOM8pw$FwPRk27+h3gw7xcskZUOBUYLN1n/YnxOVRSOsEs6c7M','Registered','2026-02-04 20:36:20','2026-03-12 13:14:25'),(5,'Test12345','Test1@gmail.com','$2b$12$d0VinwQX4n4HaoOYD9SK0evS5JX9grV//cG.YhVZO39LnmvvLH2ye','Registered','2026-02-05 12:10:46','2026-02-05 12:10:46'),(6,'dalton','daltontate22@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$ce79H0MIgRAiZMz531srxQ$eOSjKsyUTj9TL5l8iVjb1Pba0zUmCUeg3YJM4w6xn+o','Registered','2026-02-12 13:06:24','2026-02-26 12:57:02'),(7,'EpicTest','EpicTest@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$gDAmRAiB8F7r3buXUsp5Tw$92FObZKc7TA57BTEJgQjfzV0NLSd9wL2igr8y7spi6s','Registered','2026-02-18 13:51:07','2026-02-18 13:51:07'),(9,'EpicTest2','EpicTest2@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$ZuxdKyXE2DsHQIgxplTKeQ$hKxGiHjhqzmJNlVdS7gJK9fsQP41VATFppzdLDA6tdg','Registered','2026-02-18 13:51:44','2026-02-18 13:51:44'),(10,'HelloTest','Hello@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$WSslBGAMoRSCMGZMCeHc2w$qcGIAs2S+Pywwj6GgETHjQTrnv5qEZHr31GK6qAcp0U','Registered','2026-02-26 13:13:52','2026-02-26 13:13:52'),(11,'Midterm','Midterm@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$kdI6h/Dem1NK6b1X6j2HkA$/VWNvPIqdshqI9lzBPpl5dneuPQw0gocfpbLDe0Xn98','Registered','2026-03-08 16:33:10','2026-03-08 16:34:25'),(12,'Midterm1','Midterm1@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$mLNWSmltrbX23nsv5XwvpQ$MlQCsmfML1hWzMud1IR/1jzk9Etq+bX0MueBw45JsOE','Registered','2026-03-08 16:37:44','2026-03-08 16:38:51'),(13,'Midterm2','Midterm2@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$d06JMaYUYgyh9N4bIyQkBA$4NYJGpvVYgGZf/HJY3Dj2ucxjVw4DrtdO8UMTJJmiT8','Registered','2026-03-12 13:13:17','2026-03-12 13:13:17');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alignment`
--

DROP TABLE IF EXISTS `alignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alignment` (
  `AlignmentID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) NOT NULL,
  `Description` text,
  PRIMARY KEY (`AlignmentID`),
  UNIQUE KEY `ux_alignment_name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alignment`
--

LOCK TABLES `alignment` WRITE;
/*!40000 ALTER TABLE `alignment` DISABLE KEYS */;
INSERT INTO `alignment` VALUES (1,'Lawful Good','Acts with honor and compassion.'),(2,'Neutral Good','Does the best good possible.'),(3,'Chaotic Good','Acts with freedom and kindness.'),(4,'Lawful Neutral','Follows law, tradition, or code.'),(5,'True Neutral','Balanced between all forces.'),(6,'Chaotic Neutral','Follows personal freedom.'),(7,'Lawful Evil','Uses law for selfish gain.'),(8,'Neutral Evil','Does whatever benefits them.'),(9,'Chaotic Evil','Acts with selfish chaos.');
/*!40000 ALTER TABLE `alignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `background`
--

DROP TABLE IF EXISTS `background`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `background` (
  `BackgroundID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Description` text,
  PRIMARY KEY (`BackgroundID`),
  UNIQUE KEY `ux_background_name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `background`
--

LOCK TABLES `background` WRITE;
/*!40000 ALTER TABLE `background` DISABLE KEYS */;
INSERT INTO `background` VALUES (1,'Acolyte','You have spent your life in the service of a temple to a specific god or pantheon of gods. You act as an intermediary between the realm of the holy and the mortal world, performing sacred rites and offering sacrifices in order to conduct worshipers into the presence of the divine. You are not necessarily a cleric – performing sacred rites is not the same thing as channeling divine power.');
/*!40000 ALTER TABLE `background` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backgroundfeature`
--

DROP TABLE IF EXISTS `backgroundfeature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backgroundfeature` (
  `BackgroundFeatureID` int NOT NULL AUTO_INCREMENT,
  `BackgroundID` int NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Description` text,
  PRIMARY KEY (`BackgroundFeatureID`),
  KEY `BackgroundID` (`BackgroundID`),
  CONSTRAINT `backgroundfeature_ibfk_1` FOREIGN KEY (`BackgroundID`) REFERENCES `background` (`BackgroundID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backgroundfeature`
--

LOCK TABLES `backgroundfeature` WRITE;
/*!40000 ALTER TABLE `backgroundfeature` DISABLE KEYS */;
/*!40000 ALTER TABLE `backgroundfeature` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_currency`
--

DROP TABLE IF EXISTS `character_currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_currency` (
  `CharacterID` int NOT NULL,
  `CP` int NOT NULL DEFAULT '0',
  `SP` int NOT NULL DEFAULT '0',
  `EP` int NOT NULL DEFAULT '0',
  `GP` int NOT NULL DEFAULT '0',
  `PP` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `fk_character_currency_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_currency`
--

LOCK TABLES `character_currency` WRITE;
/*!40000 ALTER TABLE `character_currency` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_custom_currency`
--

DROP TABLE IF EXISTS `character_custom_currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_custom_currency` (
  `CharacterCustomCurrencyID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Amount` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`CharacterCustomCurrencyID`),
  KEY `CharacterID` (`CharacterID`),
  CONSTRAINT `fk_character_custom_currency_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_custom_currency`
--

LOCK TABLES `character_custom_currency` WRITE;
/*!40000 ALTER TABLE `character_custom_currency` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_custom_currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_equipment`
--

DROP TABLE IF EXISTS `character_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_equipment` (
  `CharacterEquipmentID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `EquipmentID` int NOT NULL,
  `Quantity` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`CharacterEquipmentID`),
  KEY `CharacterID` (`CharacterID`),
  KEY `EquipmentID` (`EquipmentID`),
  CONSTRAINT `character_equipment_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE,
  CONSTRAINT `character_equipment_ibfk_2` FOREIGN KEY (`EquipmentID`) REFERENCES `equipment` (`EquipmentID`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_equipment`
--

LOCK TABLES `character_equipment` WRITE;
/*!40000 ALTER TABLE `character_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_feat`
--

DROP TABLE IF EXISTS `character_feat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_feat` (
  `CharacterFeatID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `FeatID` int NOT NULL,
  PRIMARY KEY (`CharacterFeatID`),
  KEY `CharacterID` (`CharacterID`),
  KEY `FeatID` (`FeatID`),
  CONSTRAINT `character_feat_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE,
  CONSTRAINT `character_feat_ibfk_2` FOREIGN KEY (`FeatID`) REFERENCES `feat` (`FeatID`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_feat`
--

LOCK TABLES `character_feat` WRITE;
/*!40000 ALTER TABLE `character_feat` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_feat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_feats`
--

DROP TABLE IF EXISTS `character_feats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_feats` (
  `CharacterFeatID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `FeatID` int DEFAULT NULL,
  `CustomName` varchar(100) DEFAULT NULL,
  `CustomDescription` text,
  `PlayerNotes` text,
  PRIMARY KEY (`CharacterFeatID`),
  KEY `CharacterID` (`CharacterID`),
  KEY `FeatID` (`FeatID`),
  CONSTRAINT `fk_character_feats_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE,
  CONSTRAINT `fk_character_feats_feat` FOREIGN KEY (`FeatID`) REFERENCES `feat` (`FeatID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_feats`
--

LOCK TABLES `character_feats` WRITE;
/*!40000 ALTER TABLE `character_feats` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_feats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_features`
--

DROP TABLE IF EXISTS `character_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_features` (
  `FeatureID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `Source` varchar(50) NOT NULL,
  `SourceName` varchar(100) NOT NULL,
  `LevelGained` int NOT NULL,
  `FeatureName` varchar(255) NOT NULL,
  PRIMARY KEY (`FeatureID`),
  KEY `CharacterID` (`CharacterID`),
  CONSTRAINT `character_features_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_features`
--

LOCK TABLES `character_features` WRITE;
/*!40000 ALTER TABLE `character_features` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_inventory`
--

DROP TABLE IF EXISTS `character_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_inventory` (
  `CharacterInventoryID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `ItemName` varchar(100) NOT NULL,
  `Quantity` int NOT NULL DEFAULT '1',
  `Weight` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`CharacterInventoryID`),
  KEY `CharacterID` (`CharacterID`),
  CONSTRAINT `fk_character_inventory_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_inventory`
--

LOCK TABLES `character_inventory` WRITE;
/*!40000 ALTER TABLE `character_inventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_notes`
--

DROP TABLE IF EXISTS `character_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_notes` (
  `CharacterID` int NOT NULL,
  `Notes` text,
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `fk_character_notes_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_notes`
--

LOCK TABLES `character_notes` WRITE;
/*!40000 ALTER TABLE `character_notes` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_personality`
--

DROP TABLE IF EXISTS `character_personality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_personality` (
  `PersonalityID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `Type` enum('Trait','Ideal','Bond','Flaw') NOT NULL,
  `Description` varchar(255) NOT NULL,
  PRIMARY KEY (`PersonalityID`),
  KEY `CharacterID` (`CharacterID`),
  CONSTRAINT `character_personality_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_personality`
--

LOCK TABLES `character_personality` WRITE;
/*!40000 ALTER TABLE `character_personality` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_personality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_proficiency`
--

DROP TABLE IF EXISTS `character_proficiency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_proficiency` (
  `CharacterProficiencyID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `ProficiencyID` int NOT NULL,
  PRIMARY KEY (`CharacterProficiencyID`),
  KEY `CharacterID` (`CharacterID`),
  KEY `ProficiencyID` (`ProficiencyID`),
  CONSTRAINT `character_proficiency_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE,
  CONSTRAINT `character_proficiency_ibfk_2` FOREIGN KEY (`ProficiencyID`) REFERENCES `proficiency` (`ProficiencyID`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_proficiency`
--

LOCK TABLES `character_proficiency` WRITE;
/*!40000 ALTER TABLE `character_proficiency` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_proficiency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_resistances`
--

DROP TABLE IF EXISTS `character_resistances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_resistances` (
  `CharacterID` int NOT NULL,
  `Resistances` text,
  `Immunities` text,
  `Vulnerabilities` text,
  `Conditions` text,
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `character_resistances_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_resistances`
--

LOCK TABLES `character_resistances` WRITE;
/*!40000 ALTER TABLE `character_resistances` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_resistances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_spell`
--

DROP TABLE IF EXISTS `character_spell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_spell` (
  `CharacterSpellID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `SpellID` int NOT NULL,
  PRIMARY KEY (`CharacterSpellID`),
  KEY `CharacterID` (`CharacterID`),
  KEY `SpellID` (`SpellID`),
  CONSTRAINT `character_spell_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE,
  CONSTRAINT `character_spell_ibfk_2` FOREIGN KEY (`SpellID`) REFERENCES `spell` (`SpellID`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_spell`
--

LOCK TABLES `character_spell` WRITE;
/*!40000 ALTER TABLE `character_spell` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_spell` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_spells`
--

DROP TABLE IF EXISTS `character_spells`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_spells` (
  `CharacterSpellID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `SpellID` int DEFAULT NULL,
  `CustomName` varchar(100) DEFAULT NULL,
  `CustomLevel` int DEFAULT NULL,
  `CustomSchool` varchar(50) DEFAULT NULL,
  `CustomDescription` text,
  PRIMARY KEY (`CharacterSpellID`),
  KEY `CharacterID` (`CharacterID`),
  KEY `SpellID` (`SpellID`),
  CONSTRAINT `fk_character_spells_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE,
  CONSTRAINT `fk_character_spells_spell` FOREIGN KEY (`SpellID`) REFERENCES `spell` (`SpellID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_spells`
--

LOCK TABLES `character_spells` WRITE;
/*!40000 ALTER TABLE `character_spells` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_spells` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_subclasses`
--

DROP TABLE IF EXISTS `character_subclasses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_subclasses` (
  `CharacterID` int NOT NULL,
  `SubclassID` int NOT NULL,
  PRIMARY KEY (`CharacterID`,`SubclassID`),
  KEY `SubclassID` (`SubclassID`),
  CONSTRAINT `character_subclasses_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE,
  CONSTRAINT `character_subclasses_ibfk_2` FOREIGN KEY (`SubclassID`) REFERENCES `subclass` (`SubclassID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_subclasses`
--

LOCK TABLES `character_subclasses` WRITE;
/*!40000 ALTER TABLE `character_subclasses` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_subclasses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `character_traits`
--

DROP TABLE IF EXISTS `character_traits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character_traits` (
  `CharacterTraitID` int NOT NULL AUTO_INCREMENT,
  `CharacterID` int NOT NULL,
  `Type` enum('Trait','Ideal','Bond','Flaw') NOT NULL,
  `Description` text NOT NULL,
  PRIMARY KEY (`CharacterTraitID`),
  KEY `CharacterID` (`CharacterID`),
  CONSTRAINT `fk_character_traits_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character_traits`
--

LOCK TABLES `character_traits` WRITE;
/*!40000 ALTER TABLE `character_traits` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_traits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `characterinventory`
--

DROP TABLE IF EXISTS `characterinventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `characterinventory` (
  `CharacterID` int NOT NULL,
  `CP` int DEFAULT '0',
  `SP` int DEFAULT '0',
  `EP` int DEFAULT '0',
  `GP` int DEFAULT '0',
  `PP` int DEFAULT '0',
  `Armor` text,
  `Weapons` text,
  `Tools` text,
  `MiscItems` text,
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `characterinventory_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `characterinventory`
--

LOCK TABLES `characterinventory` WRITE;
/*!40000 ALTER TABLE `characterinventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `characterinventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `characters`
--

DROP TABLE IF EXISTS `characters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `characters` (
  `CharacterID` int NOT NULL AUTO_INCREMENT,
  `AccountID` int NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Gender` varchar(50) DEFAULT 'Unspecified',
  `Level` int NOT NULL DEFAULT '1',
  `RaceID` int NOT NULL,
  `ClassID` int NOT NULL,
  `BackgroundID` int DEFAULT NULL,
  `AlignmentID` int DEFAULT NULL,
  `Experience` int NOT NULL DEFAULT '0',
  `ProficiencyBonus` int DEFAULT NULL,
  `ProfileIconURL` varchar(255) DEFAULT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `PlayerName` varchar(255) DEFAULT NULL,
  `SubclassID` int DEFAULT NULL,
  PRIMARY KEY (`CharacterID`),
  KEY `AccountID` (`AccountID`),
  KEY `RaceID` (`RaceID`),
  KEY `ClassID` (`ClassID`),
  KEY `BackgroundID` (`BackgroundID`),
  KEY `AlignmentID` (`AlignmentID`),
  KEY `fk_character_subclass` (`SubclassID`),
  CONSTRAINT `fk_account` FOREIGN KEY (`AccountID`) REFERENCES `account` (`AccountID`) ON DELETE CASCADE,
  CONSTRAINT `fk_alignment` FOREIGN KEY (`AlignmentID`) REFERENCES `alignment` (`AlignmentID`) ON DELETE SET NULL,
  CONSTRAINT `fk_background` FOREIGN KEY (`BackgroundID`) REFERENCES `background` (`BackgroundID`) ON DELETE SET NULL,
  CONSTRAINT `fk_character_subclass` FOREIGN KEY (`SubclassID`) REFERENCES `subclass` (`SubclassID`),
  CONSTRAINT `fk_class` FOREIGN KEY (`ClassID`) REFERENCES `class` (`ClassID`) ON DELETE RESTRICT,
  CONSTRAINT `fk_race` FOREIGN KEY (`RaceID`) REFERENCES `race` (`RaceID`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `characters`
--

LOCK TABLES `characters` WRITE;
/*!40000 ALTER TABLE `characters` DISABLE KEYS */;
/*!40000 ALTER TABLE `characters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charactersavingthrows`
--

DROP TABLE IF EXISTS `charactersavingthrows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `charactersavingthrows` (
  `CharacterID` int NOT NULL,
  `StrProf` tinyint(1) NOT NULL DEFAULT '0',
  `StrValue` int DEFAULT NULL,
  `DexProf` tinyint(1) NOT NULL DEFAULT '0',
  `DexValue` int DEFAULT NULL,
  `ConProf` tinyint(1) NOT NULL DEFAULT '0',
  `ConValue` int DEFAULT NULL,
  `IntProf` tinyint(1) NOT NULL DEFAULT '0',
  `IntValue` int DEFAULT NULL,
  `WisProf` tinyint(1) NOT NULL DEFAULT '0',
  `WisValue` int DEFAULT NULL,
  `ChaProf` tinyint(1) NOT NULL DEFAULT '0',
  `ChaValue` int DEFAULT NULL,
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `fk_charactersavingthrows_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charactersavingthrows`
--

LOCK TABLES `charactersavingthrows` WRITE;
/*!40000 ALTER TABLE `charactersavingthrows` DISABLE KEYS */;
/*!40000 ALTER TABLE `charactersavingthrows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `characterskills`
--

DROP TABLE IF EXISTS `characterskills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `characterskills` (
  `CharacterID` int NOT NULL,
  `AcrobaticsProf` tinyint(1) NOT NULL DEFAULT '0',
  `AcrobaticsValue` int DEFAULT NULL,
  `AnimalHandlingProf` tinyint(1) NOT NULL DEFAULT '0',
  `AnimalHandlingValue` int DEFAULT NULL,
  `ArcanaProf` tinyint(1) NOT NULL DEFAULT '0',
  `ArcanaValue` int DEFAULT NULL,
  `AthleticsProf` tinyint(1) NOT NULL DEFAULT '0',
  `AthleticsValue` int DEFAULT NULL,
  `DeceptionProf` tinyint(1) NOT NULL DEFAULT '0',
  `DeceptionValue` int DEFAULT NULL,
  `HistoryProf` tinyint(1) NOT NULL DEFAULT '0',
  `HistoryValue` int DEFAULT NULL,
  `InsightProf` tinyint(1) NOT NULL DEFAULT '0',
  `InsightValue` int DEFAULT NULL,
  `IntimidationProf` tinyint(1) NOT NULL DEFAULT '0',
  `IntimidationValue` int DEFAULT NULL,
  `InvestigationProf` tinyint(1) NOT NULL DEFAULT '0',
  `InvestigationValue` int DEFAULT NULL,
  `MedicineProf` tinyint(1) NOT NULL DEFAULT '0',
  `MedicineValue` int DEFAULT NULL,
  `NatureProf` tinyint(1) NOT NULL DEFAULT '0',
  `NatureValue` int DEFAULT NULL,
  `PerceptionProf` tinyint(1) NOT NULL DEFAULT '0',
  `PerceptionValue` int DEFAULT NULL,
  `PerformanceProf` tinyint(1) NOT NULL DEFAULT '0',
  `PerformanceValue` int DEFAULT NULL,
  `PersuasionProf` tinyint(1) NOT NULL DEFAULT '0',
  `PersuasionValue` int DEFAULT NULL,
  `ReligionProf` tinyint(1) NOT NULL DEFAULT '0',
  `ReligionValue` int DEFAULT NULL,
  `SleightOfHandProf` tinyint(1) NOT NULL DEFAULT '0',
  `SleightOfHandValue` int DEFAULT NULL,
  `StealthProf` tinyint(1) NOT NULL DEFAULT '0',
  `StealthValue` int DEFAULT NULL,
  `SurvivalProf` tinyint(1) NOT NULL DEFAULT '0',
  `SurvivalValue` int DEFAULT NULL,
  PRIMARY KEY (`CharacterID`),
  UNIQUE KEY `CharacterID` (`CharacterID`),
  CONSTRAINT `fk_characterskills_character` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `characterskills`
--

LOCK TABLES `characterskills` WRITE;
/*!40000 ALTER TABLE `characterskills` DISABLE KEYS */;
/*!40000 ALTER TABLE `characterskills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `characterspells`
--

DROP TABLE IF EXISTS `characterspells`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `characterspells` (
  `CharacterID` int NOT NULL,
  `SpellcastingAbility` varchar(50) DEFAULT NULL,
  `SpellSaveDC` int DEFAULT NULL,
  `SpellAttackBonus` int DEFAULT NULL,
  `L1SlotsTotal` int DEFAULT '0',
  `L1SlotsRemaining` int DEFAULT '0',
  `L2SlotsTotal` int DEFAULT '0',
  `L2SlotsRemaining` int DEFAULT '0',
  `L3SlotsTotal` int DEFAULT '0',
  `L3SlotsRemaining` int DEFAULT '0',
  `L4SlotsTotal` int DEFAULT '0',
  `L4SlotsRemaining` int DEFAULT '0',
  `L5SlotsTotal` int DEFAULT '0',
  `L5SlotsRemaining` int DEFAULT '0',
  `L6SlotsTotal` int DEFAULT '0',
  `L6SlotsRemaining` int DEFAULT '0',
  `L7SlotsTotal` int DEFAULT '0',
  `L7SlotsRemaining` int DEFAULT '0',
  `L8SlotsTotal` int DEFAULT '0',
  `L8SlotsRemaining` int DEFAULT '0',
  `L9SlotsTotal` int DEFAULT '0',
  `L9SlotsRemaining` int DEFAULT '0',
  `KnownSpells` text,
  `PreparedSpells` text,
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `characterspells_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `characterspells`
--

LOCK TABLES `characterspells` WRITE;
/*!40000 ALTER TABLE `characterspells` DISABLE KEYS */;
/*!40000 ALTER TABLE `characterspells` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charactertraits`
--

DROP TABLE IF EXISTS `charactertraits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `charactertraits` (
  `CharacterID` int NOT NULL,
  `Feats` text,
  `RaceFeatures` text,
  `ClassFeatures` text,
  `BackgroundFeatures` text,
  `ProficienciesLanguages` text,
  `PersonalityTraits` text,
  `Ideals` text,
  `Bonds` text,
  `Flaws` text,
  `Backstory` text,
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `charactertraits_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charactertraits`
--

LOCK TABLES `charactertraits` WRITE;
/*!40000 ALTER TABLE `charactertraits` DISABLE KEYS */;
/*!40000 ALTER TABLE `charactertraits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `ClassID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `HitDiceType` varchar(10) DEFAULT NULL,
  `Spellcasting` tinyint(1) NOT NULL DEFAULT '0',
  `SpellcastingAbility` varchar(10) DEFAULT NULL,
  `SpellcastingType` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ClassID`),
  UNIQUE KEY `ux_class_name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'Artificer',NULL,0,NULL,NULL),(2,'Fighter',NULL,0,NULL,NULL);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_spellcasting`
--

DROP TABLE IF EXISTS `class_spellcasting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_spellcasting` (
  `ClassID` int NOT NULL,
  `Level` int NOT NULL,
  `Slots1` int DEFAULT '0',
  `Slots2` int DEFAULT '0',
  `Slots3` int DEFAULT '0',
  `Slots4` int DEFAULT '0',
  `Slots5` int DEFAULT '0',
  `Slots6` int DEFAULT '0',
  `Slots7` int DEFAULT '0',
  `Slots8` int DEFAULT '0',
  `Slots9` int DEFAULT '0',
  PRIMARY KEY (`ClassID`,`Level`),
  CONSTRAINT `class_spellcasting_ibfk_1` FOREIGN KEY (`ClassID`) REFERENCES `class` (`ClassID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_spellcasting`
--

LOCK TABLES `class_spellcasting` WRITE;
/*!40000 ALTER TABLE `class_spellcasting` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_spellcasting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classfeature`
--

DROP TABLE IF EXISTS `classfeature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classfeature` (
  `FeatureID` int NOT NULL AUTO_INCREMENT,
  `ClassID` int NOT NULL,
  `SubclassID` int DEFAULT NULL,
  `Name` varchar(50) NOT NULL,
  `Description` text,
  `EffectJson` json DEFAULT NULL,
  PRIMARY KEY (`FeatureID`),
  KEY `ClassID` (`ClassID`),
  KEY `SubclassID` (`SubclassID`),
  CONSTRAINT `classfeature_ibfk_1` FOREIGN KEY (`ClassID`) REFERENCES `class` (`ClassID`) ON DELETE CASCADE,
  CONSTRAINT `classfeature_ibfk_2` FOREIGN KEY (`SubclassID`) REFERENCES `subclass` (`SubclassID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classfeature`
--

LOCK TABLES `classfeature` WRITE;
/*!40000 ALTER TABLE `classfeature` DISABLE KEYS */;
/*!40000 ALTER TABLE `classfeature` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `combat_stats`
--

DROP TABLE IF EXISTS `combat_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `combat_stats` (
  `CharacterID` int NOT NULL,
  `MaxHP` int NOT NULL DEFAULT '10',
  `CurrentHP` int NOT NULL DEFAULT '10',
  `TempHP` int NOT NULL DEFAULT '0',
  `HitDiceType` int NOT NULL DEFAULT '0',
  `HitDiceTotal` int NOT NULL DEFAULT '1',
  `HitDiceRemaining` int NOT NULL DEFAULT '1',
  `ArmorClass` int NOT NULL DEFAULT '10',
  `Initiative` int NOT NULL DEFAULT '0',
  `Speed` int NOT NULL DEFAULT '30',
  `SpeedClimb` int NOT NULL DEFAULT '0',
  `SpeedSwim` int NOT NULL DEFAULT '0',
  `SpeedFly` int NOT NULL DEFAULT '0',
  `PassivePerception` int NOT NULL DEFAULT '0',
  `PassiveInvestigation` int NOT NULL DEFAULT '0',
  `PassiveInsight` int NOT NULL DEFAULT '0',
  `DeathSuccess1` tinyint(1) NOT NULL DEFAULT '0',
  `DeathSuccess2` tinyint(1) NOT NULL DEFAULT '0',
  `DeathSuccess3` tinyint(1) NOT NULL DEFAULT '0',
  `DeathFail1` tinyint(1) NOT NULL DEFAULT '0',
  `DeathFail2` tinyint(1) NOT NULL DEFAULT '0',
  `DeathFail3` tinyint(1) NOT NULL DEFAULT '0',
  `Resistances` text,
  `Immunities` text,
  `Vulnerabilities` text,
  `Conditions` text,
  `ProficiencyBonus` int NOT NULL DEFAULT '0',
  `Money` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `combat_stats_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combat_stats`
--

LOCK TABLES `combat_stats` WRITE;
/*!40000 ALTER TABLE `combat_stats` DISABLE KEYS */;
/*!40000 ALTER TABLE `combat_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `death_saves`
--

DROP TABLE IF EXISTS `death_saves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `death_saves` (
  `CharacterID` int NOT NULL,
  `Success1` tinyint(1) NOT NULL DEFAULT '0',
  `Success2` tinyint(1) NOT NULL DEFAULT '0',
  `Success3` tinyint(1) NOT NULL DEFAULT '0',
  `Failure1` tinyint(1) NOT NULL DEFAULT '0',
  `Failure2` tinyint(1) NOT NULL DEFAULT '0',
  `Failure3` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `death_saves_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `death_saves`
--

LOCK TABLES `death_saves` WRITE;
/*!40000 ALTER TABLE `death_saves` DISABLE KEYS */;
/*!40000 ALTER TABLE `death_saves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `EquipmentID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Type` varchar(30) DEFAULT NULL,
  `Properties` varchar(255) DEFAULT NULL,
  `Weight` decimal(6,2) DEFAULT NULL,
  `CostDesc` varchar(50) DEFAULT NULL,
  `DamageDice` varchar(20) DEFAULT NULL,
  `DamageType` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`EquipmentID`),
  UNIQUE KEY `ux_equipment_name` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feat`
--

DROP TABLE IF EXISTS `feat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feat` (
  `FeatID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Description` text,
  `Prerequisite` varchar(100) DEFAULT NULL,
  `EffectJson` json DEFAULT NULL,
  PRIMARY KEY (`FeatID`),
  UNIQUE KEY `ux_feat_name` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feat`
--

LOCK TABLES `feat` WRITE;
/*!40000 ALTER TABLE `feat` DISABLE KEYS */;
/*!40000 ALTER TABLE `feat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proficiency`
--

DROP TABLE IF EXISTS `proficiency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proficiency` (
  `ProficiencyID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Type` enum('Skill','SavingThrow','Tool','Armor','Weapon','Language','Item') NOT NULL,
  PRIMARY KEY (`ProficiencyID`),
  UNIQUE KEY `ux_proficiency_name_type` (`Name`,`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proficiency`
--

LOCK TABLES `proficiency` WRITE;
/*!40000 ALTER TABLE `proficiency` DISABLE KEYS */;
/*!40000 ALTER TABLE `proficiency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `race`
--

DROP TABLE IF EXISTS `race`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `race` (
  `RaceID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Description` text,
  PRIMARY KEY (`RaceID`),
  UNIQUE KEY `ux_race_name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `race`
--

LOCK TABLES `race` WRITE;
/*!40000 ALTER TABLE `race` DISABLE KEYS */;
INSERT INTO `race` VALUES (1,'Human','In the reckonings of most worlds, humans are the youngest of the common races, late to arrive on the world scene and short-lived in comparison to dwarves, elves, and dragons. Perhaps it is because of their shorter lives that they strive to achieve as much as they can in the years they are given. Or maybe they feel they have something to prove to the elder races, and that\'s why they build their mighty empires on the foundation of conquest and trade. Whatever drives them, humans are the innovators, the achievers, and the pioneers of the worlds.');
/*!40000 ALTER TABLE `race` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raceability`
--

DROP TABLE IF EXISTS `raceability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raceability` (
  `RaceAbilityID` int NOT NULL AUTO_INCREMENT,
  `RaceID` int NOT NULL,
  `AbilityName` varchar(50) NOT NULL,
  `ValueOrDesc` varchar(255) DEFAULT NULL,
  `EffectJson` json DEFAULT NULL,
  PRIMARY KEY (`RaceAbilityID`),
  KEY `RaceID` (`RaceID`),
  CONSTRAINT `raceability_ibfk_1` FOREIGN KEY (`RaceID`) REFERENCES `race` (`RaceID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raceability`
--

LOCK TABLES `raceability` WRITE;
/*!40000 ALTER TABLE `raceability` DISABLE KEYS */;
/*!40000 ALTER TABLE `raceability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spell`
--

DROP TABLE IF EXISTS `spell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spell` (
  `SpellID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Level` int NOT NULL DEFAULT '0',
  `School` varchar(30) DEFAULT NULL,
  `CastingTime` varchar(50) DEFAULT NULL,
  `Range` varchar(50) DEFAULT NULL,
  `Components` varchar(50) DEFAULT NULL,
  `Duration` varchar(50) DEFAULT NULL,
  `Description` text,
  PRIMARY KEY (`SpellID`),
  UNIQUE KEY `ux_spell_name_level` (`Name`,`Level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spell`
--

LOCK TABLES `spell` WRITE;
/*!40000 ALTER TABLE `spell` DISABLE KEYS */;
/*!40000 ALTER TABLE `spell` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spells`
--

DROP TABLE IF EXISTS `spells`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spells` (
  `SpellID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Level` int DEFAULT NULL,
  `School` varchar(255) DEFAULT NULL,
  `Range` varchar(255) DEFAULT NULL,
  `Components` varchar(255) DEFAULT NULL,
  `Duration` varchar(255) DEFAULT NULL,
  `CastingTime` varchar(255) DEFAULT NULL,
  `Description` text,
  PRIMARY KEY (`SpellID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spells`
--

LOCK TABLES `spells` WRITE;
/*!40000 ALTER TABLE `spells` DISABLE KEYS */;
/*!40000 ALTER TABLE `spells` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spellslot`
--

DROP TABLE IF EXISTS `spellslot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spellslot` (
  `CharacterID` int NOT NULL,
  `SpellLevel` tinyint NOT NULL,
  `MaxSlots` int NOT NULL DEFAULT '0',
  `UsedSlots` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`CharacterID`,`SpellLevel`),
  CONSTRAINT `spellslot_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spellslot`
--

LOCK TABLES `spellslot` WRITE;
/*!40000 ALTER TABLE `spellslot` DISABLE KEYS */;
/*!40000 ALTER TABLE `spellslot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subclass`
--

DROP TABLE IF EXISTS `subclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subclass` (
  `SubclassID` int NOT NULL AUTO_INCREMENT,
  `ClassID` int NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Description` text,
  PRIMARY KEY (`SubclassID`),
  UNIQUE KEY `ux_subclass_name_per_class` (`ClassID`,`Name`),
  CONSTRAINT `subclass_ibfk_1` FOREIGN KEY (`ClassID`) REFERENCES `class` (`ClassID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subclass`
--

LOCK TABLES `subclass` WRITE;
/*!40000 ALTER TABLE `subclass` DISABLE KEYS */;
INSERT INTO `subclass` VALUES (1,1,'No Subclass','Improves critical hits and athletic prowess.'),(4,2,'Champion',NULL),(5,1,'Champion','Improved Critical (19–20), Remarkable Athlete, Additional Fighting Style, Superior Critical (18–20), Survivor');
/*!40000 ALTER TABLE `subclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Test','dtate9@atu.edu','$2b$12$isYf8kEVwCCA8CT7r6.H1uhuF5hXfawFIZ2/wn5PXCg4dPvkWH.X6','2026-01-21 02:22:56');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'dnd'
--

--
-- Dumping routines for database 'dnd'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-31 10:35:18
