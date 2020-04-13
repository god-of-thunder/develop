CREATE DATABASE IF NOT EXISTS ptt;
USE ptt;
CREATE TABLE IF NOT EXISTS ios (author_id VARCHAR(100), author_name VARCHAR(100), title_name VARCHAR(100), published_time INT NOT NULL PRIMARY KEY,content_text LONGTEXT,canonical_url VARCHAR(100) NOT NULL,created_time VARCHAR(100) NOT NULL,update_time VARCHAR(100) NOT NULL,comment_id VARCHAR(100),comment_text LONGTEXT,comment_time INT);
CREATE USER 'root'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
