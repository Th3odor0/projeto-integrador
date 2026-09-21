# 🛠️ Assistência Técnica — Sistema de Gestão para Oficinas

Sistema desktop completo para gerenciamento de ordens de serviço em oficinas de assistência técnica, desenvolvido em **Python** com arquitetura **MVC**, banco de dados **MySQL** e interface gráfica em **Tkinter**.

---

## 📌 Sobre o projeto

Oficinas de conserto de equipamentos (eletrônicos, eletrodomésticos, informática, etc.) frequentemente controlam suas ordens de serviço em cadernos, planilhas soltas ou sistemas improvisados — o que gera perda de histórico, dificuldade em calcular valores e falta de rastreabilidade sobre peças e serviços utilizados em cada atendimento.

O **Assistência Técnica** nasceu para resolver esse problema: um sistema local, simples de instalar e usar, que organiza todo o fluxo de uma ordem de serviço — da entrada do equipamento até a entrega ao cliente — mantendo o controle de peças aplicadas, serviços prestados, formas de pagamento e garantia.

---

## 🎯 Público-alvo

- Pequenas e médias oficinas de assistência técnica (eletrônicos, celulares, informática, eletrodomésticos).
- Técnicos autônomos que precisam formalizar e organizar seus atendimentos.
- Negócios que ainda controlam ordens de serviço manualmente e querem migrar para um sistema digital sem depender de soluções em nuvem pagas ou complexas.

---

## ✨ Funcionalidades

- **Cadastro de Ordens de Serviço** — vincula cliente, funcionário responsável e equipamento, registrando problema relatado, diagnóstico técnico, status do atendimento e garantia.
- **Gestão de Clientes, Funcionários e Equipamentos** — cadastro completo de quem traz o equipamento, quem realiza o conserto e o que está sendo consertado.
- **Controle de Peças utilizadas** — cada ordem de serviço permite adicionar múltiplas peças do estoque, com quantidade e valor unitário, calculando o subtotal automaticamente.
- **Controle de Serviços prestados** — vincula os serviços realizados (mão de obra, diagnóstico, limpeza, etc.) a cada ordem, com valor cobrado individualizado.
- **Cálculo automático de valores** — o sistema soma peças e serviços para compor o valor total da ordem.
- **Histórico de status** — acompanhamento da evolução da ordem (aberta → em andamento → concluída).
- **Controle de garantia** — registro de dias de garantia por ordem de serviço.

---

## 🧱 Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)**, separando claramente as responsabilidades:

```
app/
├── core/          # Conexão com o banco de dados (Database)
├── models/        # Entidades do domínio (Cliente, Funcionario, Equipamento, OrdemServico, Peca, Servico...)
├── dao/           # Camada de acesso a dados (DAO Pattern) — isola toda a comunicação com o MySQL
├── controller/     # Regras de negócio e validações — ponte entre a View e o DAO
├── view/          # Interface gráfica em Tkinter
└── utils/         # Utilitários reutilizáveis (ex: conversão e validação de datas)
```

**Por que essa separação importa:**

- **Models** representam os dados puros, sem conhecer banco de dados ou interface.
- **DAOs** cuidam exclusivamente do SQL (INSERT, SELECT, UPDATE, DELETE), isolando o resto do sistema de detalhes do MySQL.
- **Controllers** validam entradas do usuário (datas, valores, campos obrigatórios) e orquestram a comunicação entre a tela e o banco.
- **Views** cuidam apenas da apresentação visual — não sabem nada sobre SQL ou regras de negócio.

Essa arquitetura facilita manutenção, testes e a compreensão do código por quem está aprendendo ou contribuindo com o projeto.

---

## 🗄️ Modelo de dados

Principais tabelas do banco de dados MySQL:

| Tabela                   | Descrição                                                                 |
| ------------------------ | ------------------------------------------------------------------------- |
| `clientes`               | Dados dos clientes que trazem equipamentos para conserto                  |
| `funcionarios`           | Técnicos e colaboradores da oficina                                       |
| `equipamentos`           | Equipamentos recebidos, vinculados a um cliente                           |
| `ordens_servico`         | Núcleo do sistema — entrada, diagnóstico, status, valores e garantia      |
| `pecas`                  | Estoque de peças disponíveis, com preço de venda                          |
| `servicos`               | Catálogo de serviços oferecidos, com valor padrão                         |
| `ordem_servico_pecas`    | Peças efetivamente utilizadas em cada ordem (quantidade e valor unitário) |
| `ordem_servico_servicos` | Serviços efetivamente prestados em cada ordem (valor cobrado)             |

---

## 🚀 Tecnologias utilizadas

- **Python 3** — linguagem principal do projeto
- **MySQL** — banco de dados relacional (via `mysql-connector-python`)
- **Tkinter** — interface gráfica desktop (nativo do Python)
- **python-dotenv** — carregamento de variáveis de ambiente (credenciais do banco)
- **DAO Pattern** — abstração de acesso a dados
- **Arquitetura MVC** — organização em camadas

---

## ✅ Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Python 3.10+** ([python.org](https://www.python.org/downloads/))
- **MySQL Server** (local ou remoto) — [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) ou XAMPP/WAMP
- **Git** (para clonar o repositório)
- Um cliente MySQL de sua preferência (MySQL Workbench, DBeaver, HeidiSQL, ou o próprio terminal) para criar o banco e as tabelas

> ⚠️ Como a interface é feita em **Tkinter**, é necessário rodar o projeto em um ambiente **com suporte gráfico** (desktop). Em algumas distribuições Linux é preciso instalar o pacote `python3-tk` separadamente (`sudo apt install python3-tk`).

---

## 🧭 Passo a passo — Instalação e execução

### 1. Clone o repositório

```bash
git clone https://github.com/Th3odor0/projeto-integrador.git
cd projeto-integrador
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Isso instalará `mysql-connector-python`, `python-dotenv` e `dotenv`.

### 4. Crie o banco de dados no MySQL

Acesse seu servidor MySQL e crie um banco para o projeto, por exemplo:

```sql
CREATE DATABASE assistencia_tecnica CHARACTER SET utf8mb4;
```

Em seguida, crie as tabelas listadas na seção [Modelo de dados](#️-modelo-de-dados) (clientes, funcionarios, equipamentos, ordens_servico, pecas, servicos, ordem_servico_pecas, ordem_servico_servicos), respeitando os relacionamentos entre elas.

### 5. Configure as variáveis de ambiente

Na raiz do projeto, crie um arquivo `.env` com as credenciais de conexão ao MySQL, por exemplo:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=assistencia_tecnica
```

> 📌 Os nomes exatos das variáveis esperadas são lidos em `app/core/database.py` — confirme lá se coincidem com o exemplo acima antes de rodar o sistema.

### 6. Execute a aplicação

```bash
python main.py
```

A janela principal do sistema (ERP - Assistência Técnica) deve abrir em modo maximizado. A partir do menu **Atendimento** é possível acessar Ordens de Serviço, Clientes, Funcionários, Equipamentos, Serviços e Peças.

### 7. (Opcional) Solução de problemas comuns

- **`ModuleNotFoundError: No module named 'tkinter'`** → instale o pacote do Tk para seu sistema (`sudo apt install python3-tk` no Ubuntu/Debian).
- **Erro de conexão com o MySQL** → confirme se o servidor está rodando, se as credenciais do `.env` estão corretas e se o banco criado no passo 4 existe.
- **`ModuleNotFoundError` para `mysql.connector` ou `dotenv`** → confirme que o ambiente virtual está ativado e rode novamente `pip install -r requirements.txt`.

---

## 📦 Status do projeto

🔧 Em desenvolvimento ativo — projeto de estudo com aplicação prática, construído camada por camada (models → DAOs → controllers → views).

---

## 👤 Autores

Desenvolvido por **Theodoro** ([@Th3odor0](https://github.com/Th3odor0)), **Renato** ([@renato1903-byte](https://github.com/renato1903-byte)) e **Guilherme** ([@Gu1paz](https://github.com/Gu1paz)) como projeto integrador de estudo e aplicação prática de Programação Orientada a Objetos, arquitetura MVC e integração com banco de dados em Python.
