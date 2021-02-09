-- 配置MySQL连接为utf-8
SET NAMES 'utf8';
SET CHARSET 'utf8';

-- 创建数据库
CREATE DATABASE IF NOT EXISTS pyweb DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
USE pyweb;

-- 创建表users, Manager
CREATE TABLE IF NOT EXISTS users
(
    id INT UNSIGNED NOT NULL,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password TEXT NOT NULL,
    picture TEXT NOT NULL,
    description TEXT,
    time TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY(id),
    UNIQUE KEY(email),
    UNIQUE KEY(name)
);

CREATE TABLE IF NOT EXISTS Manager
(
    id INT UNSIGNED NOT NULL,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password TEXT NOT NULL,
    PRIMARY KEY(id),
    UNIQUE KEY(email),
    UNIQUE KEY(name)
);



-- 创建表messages, bulletins
CREATE TABLE IF NOT EXISTS messages
(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    content TEXT NOT NULL,
    time TIMESTAMP DEFAULT NOW(),
    user_id INT UNSIGNED,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS bulletins
(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    content TEXT NOT NULL,
    time TIMESTAMP DEFAULT NOW(),
    manager_id INT UNSIGNED,
    PRIMARY KEY(id),
    FOREIGN KEY(manager_id) REFERENCES Manager(id)
);

-- 创建表foods, comments

CREATE TABLE IF NOT EXISTS foods
(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    picture TEXT NOT NULL,
    description TEXT,
    time TIMESTAMP DEFAULT NOW(),
    manager_id INT UNSIGNED,
    UNIQUE KEY(name),
    PRIMARY KEY(id),
    FOREIGN KEY(manager_id) REFERENCES Manager(id)
);

CREATE TABLE IF NOT EXISTS comments
(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    content TEXT NOT NULL,
    time TIMESTAMP DEFAULT NOW(),
    user_id INT UNSIGNED,
    parent_id INT UNSIGNED,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(parent_id) REFERENCES foods(id)

);






-- 设置时区为北京时间
-- 1.以下命令仅在当前会话期间有效
/*SET time_zone = '+8:00';*/
-- 2.以下命令则全局有效
SET GLOBAL time_zone = '+8:00';