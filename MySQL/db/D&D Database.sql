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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abilityscores`
--

LOCK TABLES `abilityscores` WRITE;
/*!40000 ALTER TABLE `abilityscores` DISABLE KEYS */;
INSERT INTO `abilityscores` VALUES (19,20,20,5,10,0,10,0,10,0,10,0,10,0),(20,19,20,5,10,0,10,0,10,0,10,0,10,0),(29,29,10,0,10,0,10,0,10,0,10,0,10,0),(42,42,10,0,10,0,10,0,10,0,10,0,10,0),(43,43,10,0,10,0,10,0,10,0,10,0,10,0),(44,44,10,0,10,0,10,0,10,0,10,0,10,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (3,'Test','dtate9@atu.edu','$2b$12$lYL6tDB7hGkyPwlV/Y0jEeCTRAc4QNLwP2ye.706kA/PmNLdNFkTi','Registered','2026-02-03 20:38:10','2026-02-03 20:38:10'),(4,'Test1','daltontate11@gmail.com','$2b$12$8iOerz3cmqT7eXikPV8deOdiOY556L4IEg37dDDLiBHMJ6CGaSGBm','Registered','2026-02-04 20:36:20','2026-02-10 12:24:50'),(5,'Test12345','Test1@gmail.com','$2b$12$d0VinwQX4n4HaoOYD9SK0evS5JX9grV//cG.YhVZO39LnmvvLH2ye','Registered','2026-02-05 12:10:46','2026-02-05 12:10:46');
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
  `SubclassID` int DEFAULT NULL,
  `BackgroundID` int DEFAULT NULL,
  `AlignmentID` int DEFAULT NULL,
  `Experience` int NOT NULL DEFAULT '0',
  `ProficiencyBonus` int DEFAULT NULL,
  `ProfileIconURL` varchar(255) DEFAULT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`CharacterID`),
  KEY `AccountID` (`AccountID`),
  KEY `RaceID` (`RaceID`),
  KEY `ClassID` (`ClassID`),
  KEY `SubclassID` (`SubclassID`),
  KEY `BackgroundID` (`BackgroundID`),
  KEY `AlignmentID` (`AlignmentID`),
  CONSTRAINT `fk_account` FOREIGN KEY (`AccountID`) REFERENCES `account` (`AccountID`) ON DELETE CASCADE,
  CONSTRAINT `fk_alignment` FOREIGN KEY (`AlignmentID`) REFERENCES `alignment` (`AlignmentID`) ON DELETE SET NULL,
  CONSTRAINT `fk_background` FOREIGN KEY (`BackgroundID`) REFERENCES `background` (`BackgroundID`) ON DELETE SET NULL,
  CONSTRAINT `fk_class` FOREIGN KEY (`ClassID`) REFERENCES `class` (`ClassID`) ON DELETE RESTRICT,
  CONSTRAINT `fk_race` FOREIGN KEY (`RaceID`) REFERENCES `race` (`RaceID`) ON DELETE RESTRICT,
  CONSTRAINT `fk_subclass` FOREIGN KEY (`SubclassID`) REFERENCES `subclass` (`SubclassID`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `characters`
--

LOCK TABLES `characters` WRITE;
/*!40000 ALTER TABLE `characters` DISABLE KEYS */;
INSERT INTO `characters` VALUES (19,5,'Test character','Unspecified',1,1,1,NULL,1,NULL,0,2,NULL,'2026-02-05 12:11:38','2026-02-05 12:11:38'),(20,5,'Test character','Unspecified',1,1,1,NULL,1,NULL,0,2,NULL,'2026-02-05 12:11:39','2026-02-05 12:11:39'),(29,3,'HEHE Test','HAHAHAH~!',1,1,1,NULL,1,NULL,0,2,NULL,'2026-02-08 17:37:35','2026-02-08 17:37:35'),(42,4,'Test character card 1','Test',1,1,1,NULL,1,NULL,0,2,NULL,'2026-02-11 16:15:12','2026-02-11 16:26:15'),(43,4,'Test character card 2','Test',1,1,1,NULL,1,NULL,0,2,NULL,'2026-02-11 16:26:31','2026-02-11 16:26:31'),(44,4,'Test Character card 3','Test',1,1,1,NULL,1,NULL,0,2,NULL,'2026-02-11 16:26:52','2026-02-11 16:26:52');
/*!40000 ALTER TABLE `characters` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'Artificer',NULL,0,NULL,NULL);
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
  CONSTRAINT `classfeature_ibfk_2` FOREIGN KEY (`SubclassID`) REFERENCES `subclass` (`SubclassID`) ON DELETE SET NULL
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
-- Table structure for table `combatstats`
--

DROP TABLE IF EXISTS `combatstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `combatstats` (
  `CharacterID` int NOT NULL,
  `HP` int NOT NULL DEFAULT '1',
  `MaxHP` int NOT NULL DEFAULT '1',
  `HitDiceTotal` varchar(50) DEFAULT NULL,
  `HitDiceRemaining` varchar(50) DEFAULT NULL,
  `ArmorClass` int DEFAULT NULL,
  `Speed` int DEFAULT NULL,
  `Initiative` int DEFAULT NULL,
  `PassivePerception` int DEFAULT NULL,
  `Money` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CharacterID`),
  CONSTRAINT `combatstats_ibfk_1` FOREIGN KEY (`CharacterID`) REFERENCES `characters` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combatstats`
--

LOCK TABLES `combatstats` WRITE;
/*!40000 ALTER TABLE `combatstats` DISABLE KEYS */;
/*!40000 ALTER TABLE `combatstats` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subclass`
--

LOCK TABLES `subclass` WRITE;
/*!40000 ALTER TABLE `subclass` DISABLE KEYS */;
INSERT INTO `subclass` VALUES (1,1,'No Subclass','Default placeholder subclass');
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

-- Dump completed on 2026-02-11 16:45:24
