USE db_arq;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `users` CASCADE;

DROP TABLE IF EXISTS `token_blocklist` CASCADE;

DROP TABLE IF EXISTS `alertas` CASCADE;

DROP TABLE IF EXISTS `dispositivos` CASCADE;

DROP TABLE IF EXISTS `fecha_alarma` CASCADE;

CREATE TABLE `users`(
	`k_users` VARCHAR(35) NOT NULL,
    `n_nombre` VARCHAR(75) NOT NULL,
    `n_correo` VARCHAR(55) NOT NULL,
	`n_categoria` VARCHAR(11) NOT NULL,
    `o_password` VARCHAR(205) NOT NULL
);

CREATE TABLE `token_blocklist`(
	`k_token` BIGINT UNIQUE auto_increment,
	`n_jti` VARCHAR(36) UNIQUE NOT NULL,
    `f_created` DATETIME NOT NULL
);

CREATE TABLE `alertas`(
	`k_alerta` INT NOT NULL AUTO_INCREMENT,
	`f_alerta` DATE NOT NULL,
	`o_img` LONGBLOB NOT NULL,
	PRIMARY KEY(k_alerta)
);

CREATE TABLE `fecha_alarma`(
	`k_alarma` BIGINT UNIQUE auto_increment,
	`f_config` DATE NOT NULL,
    `k_dispositivo` BIGINT NOT NULL
);

CREATE TABLE `dispositivos`(
	`k_dispositivo` BIGINT NOT NULL,
    `n_nombre` VARCHAR(200) NOT NULL,
    `k_users` VARCHAR(35) NOT NULL
);

/* PRIMARY KEYS */
ALTER TABLE `users` ADD CONSTRAINT `PK_k_users` PRIMARY KEY (k_users);

ALTER TABLE `token_blocklist` ADD CONSTRAINT `PK_k_token` PRIMARY KEY (k_token);

ALTER TABLE `fecha_alarma` ADD CONSTRAINT `PK_k_alama` PRIMARY KEY (k_alarma);

ALTER TABLE `dispositivo` ADD CONSTRAINT `PK_k_dispositivo` PRIMARY KEY (k_dispositivo);

ALTER TABLE `token_blocklist` ADD CONSTRAINT `PK_k_token` PRIMARY KEY (k_token);

/* CHECKS */

ALTER TABLE `users` ADD CONSTRAINT `CK_n_categoria` CHECK (n_categoria in ('Admin'));

SET FOREIGN_KEY_CHECKS=1; 

/*ALTER TABLE pedidos MODIFY n_observaciones LONGTEXT;*/