CREATE USER 'db_user'@'localhost' IDENTIFIED BY 'db_password';

CREATE DATABASE my_database;

GRANT ALL PRIVILEGES ON my_database.* TO 'db_user'@'%';

FLUSH PRIVILEGES;

/*UPDATE mysql.user SET host = '%' WHERE user = 'db_user';

FLUSH PRIVILEGES;*/

USE my_database;

CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstname varchar(50) NOT NULL,
    lastname varchar(50) NOT NULL,
    password_hash varchar(60) NOT NULL,
    email varchar(100) UNIQUE NOT NULL
);

INSERT INTO users(firstname, lastname, password_hash, email)
VALUES("Cristian", "Alexandru", "pass", "cristi@yahoo.com");


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
