CREATE DATABASE assistencia_tecnica;

USE assistencia_tecnica;


CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100)
);


CREATE TABLE equipamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(100),
    numero_serie VARCHAR(100),
    defeito VARCHAR(255),

    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);


CREATE TABLE ordens_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipamento_id INT NOT NULL,
    data_entrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    problema VARCHAR(255) NOT NULL,
    diagnostico TEXT,
    valor DECIMAL(10,2),
    status VARCHAR(30) NOT NULL DEFAULT 'Aberta',

    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
);