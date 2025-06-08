/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: hotel_db
-- ------------------------------------------------------
-- Server version	11.8.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `funcaoFuncionario`
--

DROP TABLE IF EXISTS `funcaoFuncionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcaoFuncionario` (
  `codFuncionario` int(11) NOT NULL,
  `funcaoFuncionario` varchar(50) NOT NULL,
  PRIMARY KEY (`codFuncionario`,`funcaoFuncionario`),
  CONSTRAINT `funcaoFuncionario_ibfk_1` FOREIGN KEY (`codFuncionario`) REFERENCES `funcionario` (`codFuncionario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcaoFuncionario`
--

LOCK TABLES `funcaoFuncionario` WRITE;
/*!40000 ALTER TABLE `funcaoFuncionario` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `funcaoFuncionario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `funcionario`
--

DROP TABLE IF EXISTS `funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionario` (
  `codFuncionario` int(11) NOT NULL AUTO_INCREMENT,
  `nomeFuncionario` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`codFuncionario`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionario`
--

LOCK TABLES `funcionario` WRITE;
/*!40000 ALTER TABLE `funcionario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `funcionario` VALUES
(1,'João Silva'),
(2,'Maria Santos'),
(3,'Carlos Oliveira'),
(4,'Ana Costa'),
(5,'Luiz Almeida'),
(6,'Paula Mendes'),
(7,'Roberto Lima'),
(8,'Fernanda Rocha'),
(9,'Bruno Teixeira');
/*!40000 ALTER TABLE `funcionario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `hospede`
--

DROP TABLE IF EXISTS `hospede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospede` (
  `cpfHospede` varchar(14) NOT NULL,
  `nomeHospede` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`cpfHospede`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospede`
--

LOCK TABLES `hospede` WRITE;
/*!40000 ALTER TABLE `hospede` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `hospede` VALUES
('11111111111','Carlos Mendes'),
('22222222222','Ana Paula'),
('33333333333','Maria Costa'),
('55555555555','Novo Hospede Teste');
/*!40000 ALTER TABLE `hospede` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `quarto`
--

DROP TABLE IF EXISTS `quarto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `quarto` (
  `numQuarto` int(11) NOT NULL AUTO_INCREMENT,
  `vlrQuarto` double DEFAULT NULL,
  `statusLimpeza` varchar(50) NOT NULL DEFAULT 'Limpo',
  PRIMARY KEY (`numQuarto`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quarto`
--

LOCK TABLES `quarto` WRITE;
/*!40000 ALTER TABLE `quarto` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `quarto` VALUES
(101,250,'Necessita limpeza'),
(102,180,'Limpo'),
(103,300,'Limpo');
/*!40000 ALTER TABLE `quarto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `quartoTipo`
--

DROP TABLE IF EXISTS `quartoTipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `quartoTipo` (
  `numQuarto` int(11) NOT NULL,
  `tipoID` int(11) NOT NULL,
  PRIMARY KEY (`numQuarto`,`tipoID`),
  KEY `tipoID` (`tipoID`),
  CONSTRAINT `quartoTipo_ibfk_1` FOREIGN KEY (`numQuarto`) REFERENCES `quarto` (`numQuarto`),
  CONSTRAINT `quartoTipo_ibfk_2` FOREIGN KEY (`tipoID`) REFERENCES `tipoQuarto` (`tipoID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quartoTipo`
--

LOCK TABLES `quartoTipo` WRITE;
/*!40000 ALTER TABLE `quartoTipo` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `quartoTipo` VALUES
(101,1),
(102,2),
(103,2);
/*!40000 ALTER TABLE `quartoTipo` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reserva`
--

DROP TABLE IF EXISTS `reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva` (
  `fk_hospede_cpfHospede` varchar(14) NOT NULL,
  `fk_quarto_numQuarto` int(11) NOT NULL,
  `dtEntrada` date NOT NULL,
  `vlrAdicional` double DEFAULT NULL,
  `dtSaida` date DEFAULT NULL,
  `formaPagamento` varchar(50) DEFAULT NULL,
  `dataCriacao` datetime DEFAULT NULL,
  PRIMARY KEY (`fk_hospede_cpfHospede`,`fk_quarto_numQuarto`,`dtEntrada`),
  KEY `fk_quarto_numQuarto` (`fk_quarto_numQuarto`),
  CONSTRAINT `reserva_ibfk_1` FOREIGN KEY (`fk_hospede_cpfHospede`) REFERENCES `hospede` (`cpfHospede`),
  CONSTRAINT `reserva_ibfk_2` FOREIGN KEY (`fk_quarto_numQuarto`) REFERENCES `quarto` (`numQuarto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `reserva` VALUES
('11111111111',101,'2025-05-06',NULL,'2025-05-10','Pix','2025-06-08 17:22:52');
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_uca1400_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`albert`@`localhost`*/ /*!50003 TRIGGER trigger_valor_adicional
BEFORE INSERT ON reserva
FOR EACH ROW
BEGIN
    IF NEW.vlrAdicional < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Valor adicional não pode ser negativo!';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_uca1400_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`albert`@`localhost`*/ /*!50003 TRIGGER trg_data_criacao
BEFORE INSERT ON reserva
FOR EACH ROW
BEGIN
    SET NEW.dataCriacao = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_uca1400_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`albert`@`localhost`*/ /*!50003 TRIGGER trg_limpeza_quarto_insert
AFTER INSERT ON reserva
FOR EACH ROW
BEGIN
    UPDATE quarto
    SET statusLimpeza = 'Necessita limpeza'
    WHERE numQuarto = NEW.fk_quarto_numQuarto;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_uca1400_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`albert`@`localhost`*/ /*!50003 TRIGGER trigger_valor_adicional_update
BEFORE UPDATE ON reserva
FOR EACH ROW
BEGIN
    IF NEW.vlrAdicional < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Valor adicional não pode ser negativo!';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_uca1400_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`albert`@`localhost`*/ /*!50003 TRIGGER trg_limpeza_quarto_update
AFTER UPDATE ON reserva
FOR EACH ROW
BEGIN
    UPDATE quarto
    SET statusLimpeza = 'Necessita limpeza'
    WHERE numQuarto = NEW.fk_quarto_numQuarto;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_uca1400_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`albert`@`localhost`*/ /*!50003 TRIGGER trg_reserva_delete_limpeza
AFTER DELETE ON reserva
FOR EACH ROW
BEGIN
    
    
    UPDATE quarto
    SET statusLimpeza = 'Sujo'
    WHERE numQuarto = OLD.fk_quarto_numQuarto;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `servico`
--

DROP TABLE IF EXISTS `servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `servico` (
  `fk_funcionario_codFuncionario` int(11) NOT NULL,
  `fk_quarto_numQuarto` int(11) NOT NULL,
  `descricaoServico` varchar(50) NOT NULL,
  PRIMARY KEY (`fk_funcionario_codFuncionario`,`fk_quarto_numQuarto`),
  KEY `fk_quarto_numQuarto` (`fk_quarto_numQuarto`),
  CONSTRAINT `servico_ibfk_1` FOREIGN KEY (`fk_funcionario_codFuncionario`) REFERENCES `funcionario` (`codFuncionario`),
  CONSTRAINT `servico_ibfk_2` FOREIGN KEY (`fk_quarto_numQuarto`) REFERENCES `quarto` (`numQuarto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servico`
--

LOCK TABLES `servico` WRITE;
/*!40000 ALTER TABLE `servico` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `servico` VALUES
(1,101,'Limpeza'),
(7,103,'Serviço de Quarto');
/*!40000 ALTER TABLE `servico` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tipoQuarto`
--

DROP TABLE IF EXISTS `tipoQuarto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipoQuarto` (
  `tipoID` int(11) NOT NULL AUTO_INCREMENT,
  `descricaoTipo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`tipoID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipoQuarto`
--

LOCK TABLES `tipoQuarto` WRITE;
/*!40000 ALTER TABLE `tipoQuarto` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tipoQuarto` VALUES
(1,'Solteiro'),
(2,'Casal');
/*!40000 ALTER TABLE `tipoQuarto` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-06-08 17:39:10
