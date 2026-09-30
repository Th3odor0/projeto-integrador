
CREATE DATABASE IF NOT EXISTS assistencia_tecnica CHARACTER SET utf8mb4;
USE assistencia_tecnica;

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL              -- o controller exige e-mail válido
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    cargo VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS equipamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(100) NOT NULL,             -- o controller exige marca, modelo e nº de série
    modelo VARCHAR(100) NOT NULL,
    numero_serie VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT fk_equipamento_cliente FOREIGN KEY (cliente_id)
        REFERENCES clientes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS pecas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    codigo VARCHAR(50) NOT NULL UNIQUE,      -- o controller exige código
    quantidade_estoque INT NOT NULL DEFAULT 0,
    preco_venda DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT ck_peca_estoque CHECK (quantidade_estoque >= 0),
    CONSTRAINT ck_peca_preco CHECK (preco_venda >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS servicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao VARCHAR(255) NOT NULL,         -- o controller exige descrição
    valor_padrao DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT ck_servico_valor CHECK (valor_padrao >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ordens_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    funcionario_id INT NOT NULL,             -- era NULL: o controller e a tela exigem funcionário
    equipamento_id INT NOT NULL,
    data_entrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_conclusao DATETIME NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'aberta',   -- minúsculo: o model só aceita minúsculas
    problema VARCHAR(255) NOT NULL,
    diagnostico TEXT NULL,
    valor_total DECIMAL(10,2) NOT NULL DEFAULT 0.00, -- o controller sempre grava um número
    forma_pagamento VARCHAR(30) NULL,
    dias_garantia INT DEFAULT 90,
    CONSTRAINT fk_os_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    CONSTRAINT fk_os_funcionario FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE RESTRICT,
    CONSTRAINT fk_os_equipamento FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id),
    CONSTRAINT ck_os_status CHECK (status IN ('aberta','em andamento','concluida','cancelada')),
    CONSTRAINT ck_os_valor CHECK (valor_total >= 0),
    CONSTRAINT ck_os_garantia CHECK (dias_garantia IS NULL OR dias_garantia >= 0),
    CONSTRAINT ck_os_datas CHECK (data_conclusao IS NULL OR data_conclusao >= data_entrada)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ordem_servico_pecas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ordem_servico_id INT NOT NULL,
    peca_id INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    valor_unitario DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_osp_os FOREIGN KEY (ordem_servico_id) REFERENCES ordens_servico(id) ON DELETE CASCADE,
    CONSTRAINT fk_osp_peca FOREIGN KEY (peca_id) REFERENCES pecas(id) ON DELETE RESTRICT,
    CONSTRAINT uq_osp UNIQUE (ordem_servico_id, peca_id),  -- a tela guarda 1 linha por peça
    CONSTRAINT ck_osp_qtd CHECK (quantidade > 0),
    CONSTRAINT ck_osp_valor CHECK (valor_unitario >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ordem_servico_servicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ordem_servico_id INT NOT NULL,
    servico_id INT NOT NULL,
    valor_cobrado DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_oss_os FOREIGN KEY (ordem_servico_id) REFERENCES ordens_servico(id) ON DELETE CASCADE,
    CONSTRAINT fk_oss_servico FOREIGN KEY (servico_id) REFERENCES servicos(id) ON DELETE RESTRICT,
    CONSTRAINT ck_oss_valor CHECK (valor_cobrado >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;