# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.17-log)
# Database: pyweb
# Generation Time: 2019-12-28 01:55:24 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table bulletins
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bulletins`;

CREATE TABLE `bulletins` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `manager_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `bulletins_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `Manager` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `bulletins` WRITE;
/*!40000 ALTER TABLE `bulletins` DISABLE KEYS */;

INSERT INTO `bulletins` (`id`, `content`, `time`, `manager_id`)
VALUES
	(1,'清真食堂开业啦！','2019-11-25 23:42:31',111),
	(2,'欢迎新同学','2019-11-27 23:14:16',111);

/*!40000 ALTER TABLE `bulletins` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table comments
# ------------------------------------------------------------

DROP TABLE IF EXISTS `comments`;

CREATE TABLE `comments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int(10) unsigned DEFAULT NULL,
  `parent_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `foods` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;

INSERT INTO `comments` (`id`, `content`, `time`, `user_id`, `parent_id`)
VALUES
	(4,'good','2019-12-03 00:04:00',161610208,6),
	(6,'虾好吃','2019-12-03 00:05:53',161610208,6),
	(7,'十三香的好吃','2019-12-03 00:06:48',161610208,4),
	(8,'不好吃','2019-12-25 14:52:57',161610208,4);

/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table foods
# ------------------------------------------------------------

DROP TABLE IF EXISTS `foods`;

CREATE TABLE `foods` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `picture` text NOT NULL,
  `description` text,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `manager_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `foods_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `Manager` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `foods` WRITE;
/*!40000 ALTER TABLE `foods` DISABLE KEYS */;

INSERT INTO `foods` (`id`, `name`, `picture`, `description`, `time`, `manager_id`)
VALUES
	(4,'麻辣小龙虾','/static/img/4jpeg','毕业季限定','2019-12-02 11:19:18',111),
	(6,'香锅虾','/static/img/jpg','麻辣香锅','2019-12-02 23:12:50',111),
	(7,'西红柿牛腩面','/static/img/7jpg','选用上等牛腩','2019-12-05 19:06:24',111),
	(16,'一套餐','/static/img/一套餐jpg','两素一荤','2019-12-05 19:42:38',111),
	(17,'111','/static/img/111jpg','test','2019-12-11 09:54:23',111),
	(18,'222','/static/img/222jpeg','test2','2019-12-11 09:54:59',111),
	(19,'qqq','/static/img/qqqjpg','www','2019-12-25 14:53:42',111);

/*!40000 ALTER TABLE `foods` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table Manager
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Manager`;

CREATE TABLE `Manager` (
  `id` int(10) unsigned NOT NULL,
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `Manager` WRITE;
/*!40000 ALTER TABLE `Manager` DISABLE KEYS */;

INSERT INTO `Manager` (`id`, `email`, `name`, `password`)
VALUES
	(1,'canteenadmin@163.com','Admin','123456'),
	(111,'qingzhen@163.com','Qingzhen','123456');

/*!40000 ALTER TABLE `Manager` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table messages
# ------------------------------------------------------------

DROP TABLE IF EXISTS `messages`;

CREATE TABLE `messages` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;

INSERT INTO `messages` (`id`, `content`, `time`, `user_id`)
VALUES
	(3,'但有的时候还是想点外卖','2019-11-28 13:59:27',161610208),
	(4,'冬天太冷啦','2019-12-05 19:04:09',161610208),
	(5,'好吃好吃','2019-12-25 14:52:39',161610208);

/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` text NOT NULL,
  `picture` text NOT NULL,
  `description` text,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `email`, `name`, `password`, `picture`, `description`, `time`)
VALUES
	(111,'a@qq.com','a','0b4e7a0e5fe84ad35fb5f95b9ceeac79','/static/img/user_normal.jpg','','2019-11-17 17:21:02'),
	(222,'b@qq.com','b','875f26fdb1cecf20ceb4ca028263dec6','/static/img/user_normal.jpg','','2019-11-17 17:52:41'),
	(333,'c@qq.com','c','c1f68ec06b490b3ecb4066b1b13a9ee9','/static/img/user_normal.jpg','','2019-11-17 18:21:16'),
	(161610208,'rizhaopanyan@163.com','panyan','e10adc3949ba59abbe56e057f20f883e','/static/img/161610208_head.png','Test','2019-11-17 16:26:07');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
