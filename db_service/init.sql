use db;

CREATE TABLE users(
    id int not null AUTO_INCREMENT,
    firstname varchar(50) NOT NULL,
    lastname varchar(50) NOT NULL,
    password_hash varchar(60) NOT NULL,
    email varchar(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

INSERT INTO users(firstname, lastname, password_hash, email)
VALUES("Cristian", "Alexandru", "pass", "cristi@yahoo.com"), ("test", "test2", "pasdf" "test@yahoo.com")


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
