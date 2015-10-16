DROP DATABASE IF EXISTS `Cqssc`;
CREATE DATABASE `Cqssc` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;

use 'Cqssc';

DROP TABLE IF EXISTS `Lottery`;
CREATE TABLE `Lottery` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `lottery_time` DATETIME,
  `lottery_day` INT UNSIGNED NOT NULL,
  `lottery_number` INT UNSIGNED NOT NULL,
  `one` INT UNSIGNED NOT NULL,
  `two` INT UNSIGNED NOT NULL,
  `three` INT UNSIGNED NOT NULL,
  `four` INT UNSIGNED NOT NULL,
  `five` INT UNSIGNED NOT NULL,
  `sum` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `LotteryMode`;
CREATE TABLE `LotteryMode` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `odd_even_count` INT UNSIGNED,
  `large_small_count` INT UNSIGNED,
  `description` TEXT,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `BettingRecord`;
CREATE TABLE `BettingRecord` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `lottery_mode` INT UNSIGNED  NOT NULL,
  `betting_time` DATETIME NOT NULL,
  `betting_money` INT UNSIGNED NOT NULL,
  `win_lose` FLOAT(4, 2) NOT NULL,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `BettingDayRecord`;
CREATE TABLE `BettingDayRecord` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `betting_time` DATETIME NOT NULL,
  `win_lose` FLOAT(4, 2) NOT NULL,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `Account`;
CREATE TABLE `Account` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255),
  `money` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;
