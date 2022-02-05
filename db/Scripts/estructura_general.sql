USE db_arq;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `users` CASCADE;

DROP TABLE IF EXISTS `token_blocklist` CASCADE;

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

/* PRIMARY KEYS */
ALTER TABLE `users` ADD CONSTRAINT `PK_k_users` PRIMARY KEY (k_users);

ALTER TABLE `token_blocklist` ADD CONSTRAINT `PK_k_token` PRIMARY KEY (k_token);

/* CHECKS */

ALTER TABLE `users` ADD CONSTRAINT `CK_n_categoria` CHECK (n_categoria in ('Admin'));

SET FOREIGN_KEY_CHECKS=1; 

/*ALTER TABLE pedidos MODIFY n_observaciones LONGTEXT;*/