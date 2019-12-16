-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema logins
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema logins
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `logins` DEFAULT CHARACTER SET utf8 ;
USE `logins` ;

-- -----------------------------------------------------
-- Table `logins`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `logins`.`usuarios` (
  `login` VARCHAR(100) NOT NULL,
  `senha` VARCHAR(64) NOT NULL,
  `grupo_root` TINYINT NOT NULL,
  PRIMARY KEY (`login`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
