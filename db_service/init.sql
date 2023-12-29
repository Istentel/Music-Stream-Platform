use db;

CREATE TABLE users(
    id int not null AUTO_INCREMENT,
    firstname varchar(120) NOT NULL,
    lastname varchar(120) NOT NULL,
    email varchar(150) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

INSERT INTO users(firstname, lastname, email)
VALUES("Cristian", "Alexandru", "cristi@yahoo.com"), ("test", "test2", "test@yahoo.com")


/* CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('cristi@yahoo.com', 'Admin123')
*/
