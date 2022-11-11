-- Prepares a Mysql server for the project

CREATE DATABASE IF NOT EXISTS tomodachi_db;
GRANT ALL PRIVILEGES ON `tomodachi_db`.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
